import sys
import itertools

import json
# import ruamel.yaml as yaml
import yaml

import os
from os.path import dirname

from widget_loader import WidgetLoader
from circuits import Worker, task, Event, Loader, Manager, handler


class go(Event):

    """test Event"""
    success = True

class la(Event):
    """test Event"""
    success = True

@handler("go_value_changed", channel="*")
def on_go_value_changed(component, value):
    print('made it to go success: {}  kwargs: {}'.format(component, value))

@handler("la_success", channel="*")
def la_success(*args, **kwargs):
    print('made it to la success: {}  kwargs: {}'.format(*args, **kwargs))

def worker(request, manager, watcher):
    worker = Worker().register(manager)
    assert watcher.wait("registered")

    def finalizer():
        worker.unregister()
        assert watcher.wait("unregistered")

    request.addfinalizer(finalizer)

    return worker

def run_flow(flowname):
    m = Manager()
    loader = WidgetLoader()
    loader.register(m)
    m.addHandler(on_go_value_changed)
    m.addHandler(la_success)
    m.start()

    config = read_config(flowname)

    # Setup log files and step ID #s.
    file_manager = loader.load('file_manager')
    file_manager.channel = 'file_manager'
    logs_n_ids = m.fire(go(config['Files'], complete=True), 'file_manager')
    m.flush()
    print("res: ", logs_n_ids)

    # Setup variable mapper
    variable_map = loader.load('variable_map')
    variable_map.channel = 'variable_map'
    res = m.fire(go(config['Variable map file'], complete=True), 'variable_map')
    m.flush()
    print("res: ", res)

#    flow_widgets = {}
#    for widget_id, widget_info in config['processes'].items():
#        # print("Loading: ", widget_id)
#        flow_widgets[widget_id] = loader.load(widget_info['component'])
#        flow_widgets[widget_id].channel = widget_id
#        # print("Loaded: ", flow_widgets[widget_id])
#        x = m.fire(go())

    m.stop()

def read_config(flowname):
    with open(flowname) as f:
        # Read the config file
        data = yaml.load(f)
    widgets = ['file_manager', 'read_file', 'variable_map']
    print('config file: ', data)
    return data

def translate(flowname):
    template = """{
                    "processes": {},
                    "connections": [],
                    "inports": {},
                    "outports": {}
                    }"""
    output = json.loads(template)
    filemanager = 'filemanager'
    output['processes'].update({filemanager: {'component': 'file_manager', 'metadata': {}}})
    readfile = 'readfile'
    output['processes'].update({readfile: {'component': 'read_file', 'metadata': {}}})
    variablemap = 'variablemap'
    output['processes'].update({variablemap: {'component': 'variable_map', 'metadata': {}}})
    with open(flowname) as f:
        # Read the config file
        data = yaml.load(f)
        print(data)
        # Set up the component lists
        initializations = []
        connections = []
        extracters = []
        replacers = []
        # Find how many repetitions need to be passed to each step
        num = len(data['Files'])
        step_widgets = []
        for sid, step, defn in zip(itertools.count(1), data['Step Order'],
                                   data['Step Definitions']):
            # Add to the component registry
            widget, widget_init = process_entry(step, sid)
            output['processes'].update(widget_init)
            # Create its column extracter
            extracter, extract_init, extract_defn = make_extracter(sid, defn['input columns'], num)
            extracters.append(extracter)
            output['processes'].update(extract_init)
            initializations.append(extract_defn)
            # Create its column replacer
            try:
                # If specific output columns are given, use those
                replacer, replace_init, replace_defn = make_replacer(sid, defn['output columns'], num)
            except KeyError:
                # Else use the input columns again
                replacer, replace_init, replace_defn = make_replacer(sid, defn['input columns'], num)
            replacers.append(replacer)
            output['processes'].update(replace_init)
            initializations.append(replace_defn)
            # Assign inputs
            for item in defn['inputs']:
                name, val = tuple(item.items())[0]
                new = data_connection('{}-{}'.format(step, sid), name.upper(), [val]*num)
                initializations.append(new)
            # Connect the elements of the step together
            connections.extend(link_step_internal(extracter, widget, replacer))
        # Give filemanager a list of files
        initializations.append(data_connection(filemanager, 'FILENAMES', data['Files']))
        # Link filemanager to readfile
        connections.append(connect(filemanager, 'CURRENT', readfile, 'FILENAME'))
        connections.append(connect(filemanager, 'FID', readfile, 'FID'))
        connections.append(connect(filemanager, 'LOGFILE', readfile, 'LOGFILE'))
        # Link readfile to variablemap
        connections.append(connect(readfile, 'DESTFILE', variablemap, 'FILENAME'))
        connections.append(connect(readfile, 'LOGFILE_OUT', variablemap, 'LOGFILE'))
        # Give variable_map the variables file
        initializations.append(data_connection(variablemap, 'MAPFILE', data['Variable map file']))
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
        initializations.extend(connections)
        output['connections'] = initializations
    return output


def dump_to_json(flowname, output):
    with open(flowname.replace('.yml', '.json'), 'w') as destination:
        json.dump(output, destination, indent=2, sort_keys=True)


def process_entry(widget, step):
    name = '{name}-{num}'.format(name=widget, num=step)
    return (name, widget)


def make_extracter(sid, cols, num):
    name = 'extracter-{num}'.format(num=sid)
    path = 'column_extract'
    init = {name: {'component': path, 'metadata': {}}}
    connect = {'src': {'data': [cols]*num}, 'tgt': {'process': name, 'port': 'COLUMNS'}}
    return (name, init, connect)


def make_replacer(sid, cols, num):
    name = 'replacer-{num}'.format(num=sid)
    path = 'column_replace'
    init = {name: {'component': path, 'metadata': {}}}
    tempmap = [{n: i for i, n in enumerate(cols)}]*num
    connect = {'src': {'data': tempmap}, 'tgt': {'process': name, 'port': 'TEMPMAP'}}
    return (name, init, connect)


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
    run_flow(flowname)
