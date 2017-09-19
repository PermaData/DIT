import argparse as ap

from dit_flow.dit_widget.config_translator import ConfigTranslator
from dit_flow.dit_widget.common.setup_logger import setup_logger
from widget_factory import WidgetFactory


class RunFlow():

    def __init__(self, flow_name):
        # Flow level information and utilities
        self.flow_name = flow_name
        self.logger = setup_logger(__name__, self.flow_name.split('.')[0] + '.log')

        self.config_translator = ConfigTranslator()
        self.config_translator.read_config(self.flow_name)
        self.widget_factory = WidgetFactory()
        self.file_manager = None
        self.variable_mapper = None

        #
        self.file_reader = None
        self.input_files = None
        self.input_manipulations = []

        self.file_writer = None
        self.output_directory = None
        self.output_manipulations = []


    def setup_utilities(self):
        self.file_manager = self.widget_factory.create_widget('file_manager')
        self.file_reader = self.widget_factory.create_widget(self.config_translator.get_reader_widget())
        self.variable_mapper = self.widget_factory.create_widget('variable_map')
        self.writer = self.widget_factory.create_widget(self.config_translator.get_reader_widget())


    def setup_widget_list(self, widget_defns):
        widget_list = []
        for widget in widget_defns:
            a_widget = self.widget_factory.create_widget(widget['widget'])
            a_widget.logger = self.logger
            a_widget.do_it = widget['do_it']
            a_widget.input_columns = widget['input_columns']
            a_widget.output_columns = widget['output_columns']
            for (input_arg_name, input_arg_value) in widget['inputs'].items():
                a_widget.set_input_arg(input_arg_name, input_arg_value)
            widget_list.append(a_widget)
        return widget_list


    def setup_input_manipulations(self):
        widget_defns = self.config_translator.get_input_manipulations()
        self.input_manipulations = self.setup_widget_list(widget_defns)


    def setup_output_manipulations(self):
        widget_defns = self.config_translator.get_output_manipulations()
        self.output_manipulations = self.setup_widget_list(widget_defns)


    def read_input_data(self, input_file):
        print('In read_input_data')
        data = self.file_reader.go([input_file])
        return data

    def do_input_manipulations(self):
        pass


    def do_output_manipulations(self):
        pass


    def write_output_file(self):
        pass


    def run(self):
        self.setup_utilities()
        self.setup_input_manipulations()
        self.setup_output_manipulations()
        self.input_files = self.config_translator.get_input_files()
        logs_n_ids = self.file_manager.go(self.input_files)
        for input_file, step_id, log_file in logs_n_ids:
            data = self.read_input_data(input_file)


def parse_arguments():
    parser = ap.ArgumentParser(description='Runs a DIT widget flow.')

    parser.add_argument('flowname', help='Flow configuration filename.')
    parser.add_argument('-m', '--mode', default='cli', help='Flow configuration filename.')

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()

    runner = RunFlow(args.flowname)
    runner.run()
