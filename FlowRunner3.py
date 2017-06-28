import sys
import itertools

import json
#import ruamel.yaml as yaml
import yaml

import os
from os.path import dirname

from widget_loader import WidgetLoader
from circuits import task, Event, Loader, Manager

loader = WidgetLoader()

def translate(filename):
    template = """{
                    "processes": {},
                    "connections": [],
                    "inports": {},
                    "outports": {}
                    }"""
    output = json.loads(template)

    # Setup circuits manager
    m = Manager()
    loader.register(m)

    # Setup log files and step ID #s.
    file_manager = loader.load('file_manager')
    file_manager.channel = 'file_manager'

    # Setup step input CSVs and logfiles.
    readfile = loader.load('read_file')
    readfile.channel = 'read_file'

    # Setup variable mapper
    variable_map = loader.load('variable_map')
    variable_map.channel = 'variable_map'

    with open(filename) as f:
        # Read the config file
        data = yaml.load(f)
        # Set up the component lists
        connections = []
        extracters = []
        replacers = []
        widgets = []
        # Find how many repetitions need to be passed to each step
        num = len(data['Files'])
        for sid, step, defn in zip(itertools.count(1), data['Step Order'],
                                   data['Step Definitions']):
            # Add to the component registry
            widget_name, widget = process_entry(step, sid)
            widgets.extend((widget_name, widget))
            # Create its column extracter
            extracter, extract_connect = make_extracter(sid, defn['input columns'], num)
            extracters.extend(extracter)

            # Create its column replacer
            try:
                # If specific output columns are given, use those
                replacer, replace_connect = make_replacer(sid, defn['output columns'], num)
            except KeyError:
                # Else use the input columns again
                replacer, replace_connect = make_replacer(sid, defn['input columns'], num)
            replacers.extend(replacer)

            # Connections are tuples

            # Assign inputs
            for item in defn['inputs']:
                name, val = tuple(item.items())[0]
                print('name: ', name, '  val: ', val)
                d_connect = {'{}-{}'.format(step, sid): (name.upper(), [val]*num)}
                print(d_connect)
                # new = data_connection('{}-{}'.format(step, sid), name.upper(), [val]*num)
                # initializations.append(new)
            # Connect the elements of the step together
            connections.extend(link_step_internal(extracter, widget, replacer))
        # Give filemanager a list of files
        connections({'file_manager': ('FILENAMES', data['Files'])}
        # initializations.append(data_connection(filemanager, 'FILENAMES', data['Files']))
        # Link filemanager to readfile
        connections.append(connect(filemanager, 'CURRENT', readfile, 'FILENAME'))
        connections.append(connect(filemanager, 'FID', readfile, 'FID'))
        connections.append(connect(filemanager, 'LOGFILE', readfile, 'LOGFILE'))
        # Link readfile to variablemap
        connections.append(connect(readfile, 'DESTFILE', variablemap, 'FILENAME'))
        connections.append(connect(readfile, 'LOGFILE_OUT', variablemap, 'LOGFILE'))
        # Give variable_map the variables file
        # initializations.append(data_connection(variablemap, 'MAPFILE', data['Variable map file']))
        # Link readfile and variablemap to the first step in the sequence
        connections.append(connect(readfile, 'FID_OUT', extracters[0], 'FID'))
        connections.append(connect(variablemap, 'STEP', extracters[0], 'SID'))
        connections.append(connect(variablemap, 'IN', extracters[0], 'DATAFILE'))
        connections.append(connect(variablemap, 'INMAP', extracters[0], 'DATAMAP'))
        connections.append(connect(variablemap, 'LOGFILE_OUT', extracters[0], 'LOGFILE'))
        connections.append(connect(variablemap, 'OUT', replacers[0], 'DESTFILE'))
        connections.append(connect(variablemap, 'OUTMAP', replacers[0], 'DESTMAP'))
        connections.append(connect(variablemap, 'CROSSMAP', replacers[0], 'CROSSMAP'))
        # Link variablemap to each step
        # for e, r in zip(extracters, replacers):
        #     connections.append(connect(variablemap, 'IN', e, 'DATAFILE'))
        #     connections.append(connect(variablemap, 'INMAP', e, 'DATAMAP'))
        #     connections.append(connect(variablemap, 'OUT', r, 'DESTFILE'))
        #     connections.append(connect(variablemap, 'OUTMAP', r, 'DESTMAP'))
        # Link steps in sequence
        for from_, to_e, to_r in zip(replacers[:-1], extracters[1:], replacers[1:]):
            connections.append(connect(from_, 'DATAFILE_OUT', to_e, 'DATAFILE'))
            connections.append(connect(from_, 'DATAMAP_OUT', to_e, 'DATAMAP'))
            connections.append(connect(from_, 'DESTFILE_OUT', to_r, 'DESTFILE'))
            connections.append(connect(from_, 'DESTMAP_OUT', to_r, 'DESTMAP'))
            connections.append(connect(from_, 'FID_OUT', to_e, 'FID'))
            connections.append(connect(from_, 'SID_OUT', to_e, 'SID'))
            connections.append(connect(from_, 'CROSSMAP_OUT', to_r, 'CROSSMAP'))
            connections.append(connect(from_, 'LOGFILE_OUT', to_e, 'LOGFILE'))
        # Put connections into output json
        # initializations.extend(connections)
        # output['connections'] = initializations
    with open(flowname, 'w') as destination:
        json.dump(output, destination, indent=2, sort_keys=True)


def process_entry(widget_name, step):
    name = '{name}-{num}'.format(name=widget_name, num=step)
    widget = loader.load(widget_name)
    return (name, widget)


def make_extracter(sid, cols, num):
    name = 'extracter-{num}'.format(num=sid)
    extracter = loader.load('column_extract')
    connect = {'src': {'data': [cols]*num}, 'tgt': {'process': extracter, 'port': 'COLUMNS'}}
    return (name, connect)


def make_replacer(sid, cols, num):
    name = 'replacer-{num}'.format(num=sid)
    replacer = loader.load('column_replace')
    tempmap = [{n: i for i, n in enumerate(cols)}]*num
    connect = {'src': {'data': tempmap}, 'tgt': {'process': replacer, 'port': 'TEMPMAP'}}
    return (name, connect)


def link_step_internal(extracter, widget, replacer):
    out = []
    out.append(connect(extracter, 'TEMPIN', widget, 'INFILE'))
    out.append(connect(extracter, 'TEMPOUT', widget, 'OUTFILE_IN'))
    out.append(connect(extracter, 'LOGFILE_OUT', widget, 'LOGFILE_IN'))

    out.append(connect(extracter, 'DATAFILE_OUT', replacer, 'DATAFILE'))
    out.append(connect(extracter, 'DATAMAP_OUT', replacer, 'DATAMAP'))
    out.append(connect(extracter, 'FID_OUT', replacer, 'FID'))
    out.append(connect(extracter, 'SID_OUT', replacer, 'SID'))

    out.append(connect(widget, 'OUTFILE_OUT', replacer, 'TEMPFILE'))

    out.append(connect(widget, 'LOGFILE_OUT', replacer, 'LOGFILE'))

    return out


def data_connection(component, port, data):
    portID = port.upper()
    return {'src': {'data': data}, 'tgt': {'process': component, 'port': portID}}


def connect(sender, sport, receiver, rport):
    src = {'process': sender, 'port': sport}
    tgt = {'process': receiver, 'port': rport}
    return {'src': src, 'tgt': tgt}


if __name__ == '__main__':
    flowname = sys.argv[1]
    translate(flowname)
