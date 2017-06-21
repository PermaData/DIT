import json

from dit_flow import config_translator as trans

configname = 'Example_config.yml'
flowname = 'Example_flow.json'

trans.translate(configname, flowname)

f = open(flowname)
data = json.load(f)

