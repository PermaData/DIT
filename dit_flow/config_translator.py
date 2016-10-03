import sys

import json
import ruamel.yaml as yaml


def translate(filename):
    template = """{
                    "processes": {},
                    "connections": [],
                    "inports": {},
                    "outports": {}
                    }"""
    output = json.loads(template)
    with open(filename) as f:
        data = yaml.load(f)
        for step, defn in zip(data['Step order'], data['Step definitions']):
            new = process_entry(step, output['processes'].keys())
            output['processes'].update(new)
            


def process_entry(widget, existing):
    template = '{name}-{number}'
    path = '/dit_widget/{name}/{name}'.format(name=widget)
    i = 1
    name = template.format(name=widget, number=i)
    while name in existing:
        name = template.format(name=widget, number=i)
        i += 1
    return {name: {'component': path, metadata: {}}}


if __name__ == '__main__':
    filename = sys.argv[1]
    translate(filename)
