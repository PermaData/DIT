import sys
import itertools

import json
import ruamel.yaml as yaml


def translate(filename, flowname):
    template = """{
                    "processes": {},
                    "connections": [],
                    "inports": {},
                    "outports": {}
                    }"""
    output = json.loads(template)
    filemanager = 'filemanager'
    output['processes'].update({filemanager: {'component': 'dit_flow/dit_widget/file_manager/file_manager', 'metadata': {}}})
    readfile = 'readfile'
    output['processes'].update({readfile: {'component': 'dit_flow/dit_widget/read_file/read_file', 'metadata': {}}})
    variablemap = 'variablemap'
    output['processes'].update({variablemap: {'component': 'dit_flow/dit_widget/variable_map/variable_map', 'metadata': {}}})
    sink = 'sink'
    output['processes'].update({sink: {'component': 'dit_flow/dit_widget/finish/finish', 'metadata': {}}})
    with open(filename) as f:
        # Read the config file
        data = yaml.load(f)
        # Set up the component lists
        initializations = []
        connections = []
        extracters = []
        replacers = []
        # Find how many repetitions need to be passed to each step
        num = len(data['Files'])
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
        # Link readfile to variablemap
        connections.append(connect(readfile, 'DESTFILE', variablemap, 'FILENAME'))
        # Give variable_map the variables file
        initializations.append(data_connection(variablemap, 'MAPFILE', data['Variable map file']))
        # Link readfile and variablemap to the first step in the sequence
        connections.append(connect(readfile, 'FID_OUT', extracters[0], 'FID'))
        connections.append(connect(variablemap, 'STEP', extracters[0], 'SID'))
        connections.append(connect(variablemap, 'IN', extracters[0], 'DATAFILE'))
        connections.append(connect(variablemap, 'INMAP', extracters[0], 'DATAMAP'))
        connections.append(connect(variablemap, 'OUT', replacers[0], 'DESTFILE'))
        connections.append(connect(variablemap, 'OUTMAP', replacers[0], 'DESTMAP'))
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
        # # Sink all open connections of the final replacer
        for portname in ['DATAFILE_OUT', 'DATAMAP_OUT', 'FID_OUT', 'SID_OUT', 'DESTFILE_OUT', 'DESTMAP_OUT']:
            connections.append(connect(replacers[-1], portname, sink, 'SINK'))
        # Put connections into output json
        initializations.extend(connections)
        output['connections'] = initializations
    with open(flowname, 'w') as destination:
        json.dump(output, destination, indent=2, sort_keys=True)


def process_entry(widget, step):
    name = '{name}-{num}'.format(name=widget, num=step)
    path = 'dit_flow/dit_widget/{name}/{name}'.format(name=widget)
    return (name, {name: {'component': path, 'metadata': {}}})


def make_extracter(sid, cols, num):
    name = 'extracter-{num}'.format(num=sid)
    path = 'dit_flow/dit_widget/column_extract/column_extract'
    init = {name: {'component': path, 'metadata': {}}}
    connect = {'src': {'data': [cols]*num}, 'tgt': {'process': name, 'port': 'COLUMNS'}}
    return (name, init, connect)


def make_replacer(sid, cols, num):
    name = 'replacer-{num}'.format(num=sid)
    path = 'dit_flow/dit_widget/column_replace/column_replace'
    init = {name: {'component': path, 'metadata': {}}}
    tempmap = [{n: i for i, n in enumerate(cols)}]*num
    connect = {'src': {'data': tempmap}, 'tgt': {'process': name, 'port': 'TEMPMAP'}}
    return (name, init, connect)


def link_step_internal(extracter, widget, replacer):
    out = []
    out.append(connect(extracter, 'TEMPIN', widget, 'INFILE'))
    out.append(connect(extracter, 'TEMPOUT', widget, 'OUTFILE_IN'))

    out.append(connect(extracter, 'DATAFILE_OUT', replacer, 'DATAFILE'))
    out.append(connect(extracter, 'DATAMAP_OUT', replacer, 'DATAMAP'))
    out.append(connect(extracter, 'FID_OUT', replacer, 'FID'))
    out.append(connect(extracter, 'SID_OUT', replacer, 'SID'))

    out.append(connect(widget, 'OUTFILE_OUT', replacer, 'TEMPFILE'))

    return out


def data_connection(component, port, data):
    portID = port.upper()
    return {'src': {'data': data}, 'tgt': {'process': component, 'port': portID}}


def connect(sender, sport, receiver, rport):
    src = {'process': sender, 'port': sport}
    tgt = {'process': receiver, 'port': rport}
    return {'src': src, 'tgt': tgt}


if __name__ == '__main__':
    filename = sys.argv[1]
    flowname = sys.argv[2]
    translate(filename, flowname)
