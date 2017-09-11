import sys
import itertools

import json
import yaml

class ConfigTranslator():
    config_file = None
    config = {}

    def set_config_file(self, config_file):
        self.config_file = config_file
        self.config = yaml.safe_load(config_file)

        print('Read in file ', config_file)
        print(self.config)

