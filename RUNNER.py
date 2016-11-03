import json

import dit_flow.rill.rill as rill

from dit_flow import config_translator as trans

configname = 'Example_config.yml'
flowname = 'Example_flow.json'

trans.translate(configname, flowname)

f = open(flowname)
data = json.load(f)

graph = rill.engine.network.Graph.from_dict(data)
net = rill.engine.network.Network(graph)

net.go()
