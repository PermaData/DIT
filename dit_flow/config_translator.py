import os
import yaml
from dit_flow.utility_widget import UtilityWidget


class ConfigTranslator(UtilityWidget):


    def __init__(self):
        super(ConfigTranslator, self).__init__()
        self.config_file = None
        self.config = None


    def read_config(self, config_file):
        self.config_file = config_file
        with open(self.config_file) as open_config:
            self.config = yaml.safe_load(open_config)

        print('Read in file ', self.config_file)
        print(self.config)
        return self.config

    def get_reader_widget(self):
        return self.config['input']['reader']

    def get_input_files(self):
        input_dir = self.config['input']['data_directory']
        files = []
        for root, dirs, all_files in os.walk(input_dir, topdown=False):
            for file in all_files:
                file_path = os.path.join(root, file)
                files.append(file_path)
        return files

    def get_variable_map(self):
        return self.config['input']['variable_map']


    def get_missing_values(self):
        return self.config['input']['missing_values']


    def get_missing_characters(self):
        return self.config['input']['missing_characters']


    def get_input_manipulations(self):
        return self.config['input']['manipulations']


    def get_output_directory(self):
        return self.config['output']['data_directory']

    def get_output_manipulations(self):
        return self.config['output']['manipulations']
