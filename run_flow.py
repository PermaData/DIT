import argparse as ap
import numpy as np
import os

from dit_flow.dit_widget.config_translator import ConfigTranslator
from dit_flow.dit_widget.common.setup_logger import setup_logger
from dit_flow.manipulation_widget import ManipulationWidget
from pathlib import Path
from widget_factory import WidgetFactory


class RunFlow():

    def __init__(self, flow_name, log_file=None):
        # Flow level information and utilities
        self.flow_name = flow_name
        if log_file is None:
            self.log_file = os.path.join(os.getcwd(), self.flow_name.split('.')[0] + '.log')
        else:
            self.log_file = log_file
        self.logger = setup_logger('', self.log_file)
        self.logger.info('Setup logging into: {}'.format(self.log_file))

        self.config_translator = ConfigTranslator()
        self.config_translator.read_config(self.flow_name)
        self.widget_factory = WidgetFactory()
        self.file_manager = None
        self.variable_mapper = None

        self.file_reader = None
        self.input_files = None
        self.input_manipulations = []

        self.file_writer = None
        self.output_directory = None
        self.output_manipulations = []

    def setup_utilities(self):
        self.logger.info('Setting up file manager widget')
        self.file_manager = self.widget_factory.create_widget('file_manager',
                                                              log_file=self.log_file)
        reader_name = self.config_translator.get_reader_widget()
        self.logger.info('Setting up reader widget: {}'.format(reader_name))
        self.file_reader = self.widget_factory.create_widget(reader_name,
                                                             log_file=self.log_file)
        self.logger.info('Setting up variable mapper widget')
        self.variable_mapper = self.widget_factory.create_widget('variable_map',
                                                                 log_file=self.log_file)
        writer_name = self.config_translator.get_writer_widget()
        self.logger.info('Setting up writer widget: {}'.format(writer_name))
        self.file_writer = self.widget_factory.create_widget(writer_name,
                                                             log_file=self.log_file)

    def setup_widget_list(self, widget_defns):
        widget_list = []
        for widget in widget_defns:
            a_widget = self.widget_factory.create_widget(
                self.config_translator.get_widget_name_from_widget_config(widget),
                log_file=self.log_file)
            a_widget.channel = self.config_translator.get_widget_name_from_widget_config(widget)
            a_widget.do_it = self.config_translator.get_do_it_from_widget_config(widget)
            a_widget.input_columns = self.config_translator.get_input_columns_from_widget_config(widget)
            a_widget.output_columns = self.config_translator.get_output_columns_from_widget_config(widget)
            a_widget.with_header = self.config_translator.get_with_header_from_widget_config(widget)
            for (input_arg_name, input_arg_value) in \
                    self.config_translator.get_input_args_from_widget_config(widget).items():
                a_widget.set_input_arg(input_arg_name, input_arg_value)
            widget_list.append(a_widget)
        return widget_list

    def setup_input_manipulations(self):
        widget_defns = self.config_translator.get_input_manipulations()
        self.input_manipulations = self.setup_widget_list(widget_defns)

    def setup_output_manipulations(self):
        widget_defns = self.config_translator.get_output_manipulations()
        self.output_manipulations = self.setup_widget_list(widget_defns)

    def can_do_subset(self, np_data, input_columns):
        can_do_subset_replace = True
        if np_data.size == 0:
            self.logger.warn('Cannot subset or replace, data is empty.')
            can_do_subset_replace = False
        if not ManipulationWidget.columns_exist(input_columns):
            self.logger.warn('Cannot subset, widget input columns missing.')
            can_do_subset_replace = False
        return can_do_subset_replace

    def can_do_replace(self, np_data, output_columns):
        can_do_subset_replace = True
        if np_data.size == 0:
            self.logger.warn('Cannot subset or replace, data is empty.')
            can_do_subset_replace = False
        if not ManipulationWidget.columns_exist(output_columns):
            self.logger.warn('Cannot replace, widget output columns missing.')
            can_do_subset_replace = False

        return can_do_subset_replace

    def read_input_data(self, input_file, log_file):
        data = self.file_reader.go(input_file, log_file=log_file)
        return np.array(data, dtype=object)

    def subset_data(self, np_data, columns, with_header=False):
        if columns == ['all']:
            columns = list(range(1, np_data.shape[1] + 1))
        zero_based_columns = [column - 1 for column in columns]
        subset_data = np_data[:, zero_based_columns]
        if with_header:
            self.logger.info('Subsetting columns with headers: {}'.format(columns))
        else:
            self.logger.info('Subsetting columns without headers: {}'.format(columns))
            subset_data = np.delete(subset_data, (0), axis=0)

        return subset_data

    def replace_data(self, np_data, manipulated_data, columns, with_header=False):
        if columns is None:
            return
        elif len(columns) == 0:
            return
        if columns == ['all']:
            columns = list(range(1, np_data.shape[0] + 1))
        zero_based_columns = [column - 1 for column in columns]
        row_start = int(not with_header)
        for row_cnt, row in enumerate(manipulated_data):
            for col_cnt, col in enumerate(zero_based_columns):
                np_data[row_start + row_cnt, col] = row[col_cnt]
        return np_data

    def set_widget_required_args(self, widget, widget_data_in_file, widget_data_out_file, log_file):
        widget.set_required_arg('input_data_file', widget_data_in_file)
        widget.set_required_arg('output_data_file', widget_data_out_file)
        widget.set_required_arg('log_file', log_file)
        return widget

    def format_to_output_data(self, input_data, variable_map, log_file):
        output_data = self.variable_mapper.go(input_data.tolist(), variable_map, log_file)
        return np.array(output_data, dtype=object)

    def do_manipulations(self, manipulations, np_data, output_dir, file_id, log_file):
        for step_id, widget in enumerate(manipulations):
            if not widget.do_it:
                return
            try:
                widget.channel = widget.channel + '_' + str(file_id) + '_' + str(step_id)
                widget_data_in_file = Path(output_dir).joinpath(widget.channel + '.in')
                widget_data_out_file = Path(output_dir).joinpath(widget.channel + '.out')
                widget = self.set_widget_required_args(widget, widget_data_in_file, widget_data_out_file, log_file)

                if self.can_do_subset(np_data, widget.input_columns):
                    # Setup subsetted data for widget manipulation
                    widget_data = self.subset_data(np_data, widget.input_columns, widget.with_header)
                    self.write_output_file(widget_data_in_file, widget_data, log_file=log_file)

                # Do manipulation
                widget.go()

                if self.can_do_replace(np_data, widget.output_columns):
                    # Reintegrate manipulated data
                    manipulated_data = self.read_input_data(widget_data_out_file, log_file)
                    np_data = self.replace_data(np_data, manipulated_data, widget.output_columns, widget.with_header)
            except Exception as ex:
                self.logger.error('{}'.format(ex))

    def write_output_file(self, output_file, np_data, log_file):
        self.file_writer.go(output_file, np_data, log_file=log_file)

    def run(self):
        self.setup_utilities()
        self.setup_input_manipulations()
        self.setup_output_manipulations()
        self.input_files = self.config_translator.get_input_files()
        self.logger.debug('Input file list:')
        for i_file in self.input_files:
            self.logger.debug('\t' + i_file)
        output_dir = self.config_translator.get_output_directory()
        temp_dir = self.config_translator.get_temp_directory()
        files_n_ids = self.file_manager.go(self.input_files, output_dir, temp_dir)
        for input_file, output_file, file_id, log_file in files_n_ids:
            self.logger.debug('Reading input data from: ' + input_file)
            input_data = self.read_input_data(input_file, log_file)
            self.logger.debug('Doing input manipulations')
            self.do_manipulations(self.input_manipulations, input_data, temp_dir, file_id, log_file)

            self.logger.debug('Translating input to output CSV.')
            mapper_vals = self.format_to_output_data(input_data,
                                                     self.config_translator.get_variable_map(),
                                                     log_file)
            output_data = np.array(mapper_vals[0], dtype=object)
            self.logger.debug('Doing output manipulations.')
            self.do_manipulations(self.output_manipulations, output_data, temp_dir, file_id, log_file)

            self.logger.debug('Writing output file.')
            self.write_output_file(output_file, output_data, log_file)


def parse_arguments():
    parser = ap.ArgumentParser(description='Runs a DIT widget flow.')

    parser.add_argument('flowname', help='Flow configuration filename.')
    parser.add_argument('-l', '--log_file', default='./run_flow.log', help='Path to log file.')
    parser.add_argument('-m', '--mode', default='cli', help='Flow configuration filename.')

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()

    runner = RunFlow(args.flowname, args.log_file)
    runner.run()
