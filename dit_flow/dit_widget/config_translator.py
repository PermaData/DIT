import collections
import logging
import os
import yaml

from pathlib import Path
from dit_flow.dit_widget.common.setup_logger import setup_logger
from dit_flow.utility_widget import UtilityWidget


class ConfigTranslator(UtilityWidget):

    config_file_path = './config.yaml'

    config = {
            'flow_name': '',
            'execution': {
                'log_file': './flow.log',
                'log_level': 'info',
                'clobber_temp_files': True,
                'clobber_output_files': False
            },
            'input': {
                'reader': 'read_csv_file',
                'data_directory': '',
                'variable_map': '',
                'missing_values': [],
                'missing_characters': [],
                'manipulations': []
            },
            'output': {
                'writer': 'write_csv_file',
                'data_directory': '',
                'temp_directory': '',
                'missing_values': [],
                'missing_characters': [],
                'manipulations': []
            }
        }

    widget = {
            'widget': '',
            'do_it': True,
            'with_hdeaer': False,
            'input_columns': [],
            'inputs': {},
            'output_columns': []
        }


    def __init__(self, *args, **kwargs):
        super(ConfigTranslator, self).__init__(*args, **kwargs)
        self.config_file = None
        self.log_file = None
        self.log_level = None

    def config_to_html_vals(self, config):
        print('config_to_html_vals input config: ', config)
        vals_to_convert = {
                'execution': {
                    'clobber_temp_files': 'on' if config['execution']['clobber_temp_files'] else 'off',
                    'clobber_output_files': 'on' if config['execution']['clobber_output_files'] else 'off'
                    },
                'input': {
                    'missing_values': ','.join(config['input']['missing_values']),
                    'missing_characters': ','.join(config['input']['missing_characters']),
                    'manipulations': config['input']['manipulations']
                    },
                'output': {
                    'missing_values':  ','.join(config['output']['missing_values']),
                    'missing_characters': ','.join(config['output']['missing_characters']),
                    'manipulations': config['input']['manipulations']
                    }
                }
        print('vals_to_convert from config_to_html_vals: ', vals_to_convert)
        self.deep_update(config, vals_to_convert)
        print('Return from config_to_html_vals: ', config)
        return config

    def html_to_config_vals(self, config):
        print('htmo_to_config_vals input config: ', config)
        updated_config = self.config.copy()
        self.deep_update(updated_config, config)
        vals_to_convert = {
                'execution': {
                    'clobber_temp_files': True if 'clobber_temp_files' in config['execution'] else False,
                    'clobber_output_files': True if 'clobber_output_files' in config['execution'] else False
                    },
                'input': {
                    'missing_values': [missing.strip() for missing in
                                       updated_config['input']['missing_values'].split(',')],
                    'missing_characters': [missing.strip() for missing in
                                           updated_config['input']['missing_characters'].split(',')],
                    'manipulations': updated_config['input']['manipulations']
                    },
                'output': {
                    'missing_values': [missing.strip() for missing in
                                       updated_config['output']['missing_values'].split(',')],
                    'missing_characters': [missing.strip() for missing in
                                           updated_config['output']['missing_characters'].split(',')],
                    'manipulations': updated_config['output']['manipulations']
                    }
                }
        print('vals_to_convert from html_to_config_vals: ', vals_to_convert)
        self.deep_update(updated_config, vals_to_convert)
        print('Return from html_to_config_vals: ', updated_config)
        return updated_config

    def read_config(self, config_file):
        self.config_file = config_file
        with open(self.config_file) as open_config:
            self.config.update(yaml.safe_load(open_config))
        self.logger = setup_logger(__name__, log_file=self.get_log_file(), log_level=self.get_log_level())
        self.logger.debug('Loaded configuration file: {}'.format(config_file))
        return self.config

    def set_log_file(self, value):
        if self.log_file is None:
            if value is None:
                self.log_file = Path.create()
            else:
                self.log_file = value

    def get_log_file(self):
        self.set_log_file(self.config['execution']['log_file'])
        return self.log_file

    def set_log_level(self, value):
        if value is None:
            self.log_level = logging.ERROR
        elif isinstance(value, str):
            self.log_level = getattr(logging, value.upper())
        else:
            self.log_level = value

    def get_log_level(self):
        self.set_log_level(self.config['execution']['log_level'])
        return self.log_level

    def get_delete_temp(self):
        return self.config['execution']['delete_temp']

    def get_delete_output(self):
        return self.config['execution']['delete_output']

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

    def get_temp_directory(self):
        temp_dir = Path(self.config['output']['temp_directory'])
        try:
            temp_dir.mkdir(mode=0o775)
        except FileExistsError:
            # Do nothing if the directory already exists.
            pass
        return str(temp_dir)

    def get_variable_map(self):
        return self.config['input']['variable_map']

    def get_missing_values(self):
        return self.config['input']['missing_values']

    def get_missing_characters(self):
        return self.config['input']['missing_characters']

    def get_input_manipulations(self):
        return self.config['input']['manipulations']

    def get_output_directory(self):
        output_dir = Path(self.config['output']['data_directory'])
        try:
            output_dir.mkdir(mode=0o775)
        except FileExistsError:
            # Do nothing if the directory already exists.
            pass
        return str(output_dir)

    def get_output_manipulations(self):
        return self.config['output']['manipulations']

    def get_info_from_widget_config(self, widget_config, key, log_key_name):
        if key in widget_config:
            return widget_config[key]
        else:
            self.logger.warn( 'No {} specified for widget.'.format(log_key_name))
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

    def deep_update(self, d, u):
        for k, v in u.items():
            if isinstance(v, collections.Mapping):
                d[k] = self.deep_update(d.get(k, {}), v)
            else:
                d[k] = v
        return d
