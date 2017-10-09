from pathlib import Path
from dit_flow.utility_widget import UtilityWidget
from dit_flow.dit_widget.common.setup_logger import setup_logger


class FileManager(UtilityWidget):

    def __init__(self, *args, **kwargs):
        super(FileManager, self).__init__(*args, **kwargs)
        self.widget_method = self.file_manager

    def file_manager(self, filenames, output_dir, temp_dir, log_file=None):
        """
        filenames: a sequence of paths to data files
        CURRENT: sends out a sequence of filenames after confirming they exist
        FID: a sequential numeric identifier for each file
        LOGFILE: sends out a sequence of log filenames that correspond to a data file
        """
        self.logger = setup_logger(__name__, log_file)
        step_files = []
        for identifier, name in enumerate(filenames, start=1):
            name_path = Path(name)
            output_dir_path = Path(output_dir)
            temp_dir_path = Path(temp_dir)
            output_filename = name_path.name.replace(name_path.suffix, '_out.csv')
            output_path = output_dir_path.joinpath(output_filename)
            log_filename = name_path.name.replace(name_path.suffix, '.log')
            log_path = temp_dir_path.joinpath(log_filename)
            try:
                # Open the file. If the file doesn't exist, the error will be
                # caught.
                if log_path.exists():
                    log_path.write_bytes(b'')
                else:
                    log_path.touch(mode=0o666)
                step_files.append((name, str(output_path), identifier, str(log_path)))
            except FileNotFoundError:
                self.logger.error('The log file {f} does not exist and cannot be created.'.format(f=str(log_path)))
        return step_files
