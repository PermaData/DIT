import os
import yaml

from dit_flow.dit_widget.common.setup_logger import setup_logger
from dit_flow.utility_widget import UtilityWidget


class ConfigTranslator(UtilityWidget):


    def __init__(self, *args, **kwargs):
        super(ConfigTranslator, self).__init__(*args, **kwargs)
        self.config_file = None
        self.config = None
        if 'log_file' not in kwargs.keys():
            kwargs['log_file'] = None
        self.logger = setup_logger(__name__, kwargs['log_file'])


    def read_config(self, config_file):
        self.logger.info('Loading configuration file: {}'.format(config_file))
        self.config_file = config_file
        with open(self.config_file) as open_config:
            self.config = yaml.safe_load(open_config)
        return self.config

    def get_reader_widget(self):
        return self.config['input']['reader']

    def get_writer_widget(self):
        return self.config['output']['writer']

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


    def get_info_from_widget_config(self, widget_config, key, log_key_name):
        if key in widget_config:
            return widget_config[key]
        else:
            self.logger.warning(
                'No {} specified for widget: {}'.format(log_key_name,
                    self.get_widget_name_from_widget_config(widget_config)))
            return None


    def get_widget_name_from_widget_config(self, widget_config):
        return self.get_info_from_widget_config(widget_config, 'widget', 'name')


    def get_input_args_from_widget_config(self, widget_config):
        return self.get_info_from_widget_config(widget_config, 'inputs', 'input arguments')


    def get_do_it_from_widget_config(self, widget_config):
        return self.get_info_from_widget_config(widget_config, 'do_it', 'do it flag')


    def get_input_columns_from_widget_config(self, widget_config):
        return self.get_info_from_widget_config(widget_config, 'input_columns', 'input columns')


    def get_output_columns_from_widget_config(self, widget_config):
        return self.get_info_from_widget_config(widget_config, 'output_columns', 'output columns')


    def get_with_header_from_widget_config(self, widget_config):
        return self.get_info_from_widget_config(widget_config, 'with_header', 'with header flag')
