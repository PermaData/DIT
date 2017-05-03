""" Reformats a file of one column of date/times into GTN-P specific date/time format. """

import csv
import datetime as dt

from circuits import Component

class ReformatDatesToGtnp(Component):

    channel = 'ReformatDatesToGtnp'

    def go(self, event):
        print(self.channel, ' received go event')

gtnp_date_time_format = '%Y-%m-%d %H:%M'

def reformat_dates_to_gtnp(INFILE, OUTFILE_IN, LOGFILE_IN, FORMAT, OUTFILE_OUT,
                           LOGFILE_OUT):
    """
    Reformat the date/times.
    :param column_file: file containing date/time column
    :param out_file: CSV filename for reformatted date/times
    :param in_format: python strptime format string of date/times in column_file
    """
    for infile, outfile, format_, logfile in zip(INFILE.iter_contents(),
                                                 OUTFILE_IN.iter_contents(),
                                                 FORMAT.iter_contents(),
                                                 LOGFILE_IN.iter_contents()):
        with open(infile, newline='') as _in, \
             open(outfile, 'w', newline='') as _out, \
             open(logfile, 'a') as _log:
            data = csv.reader(_in)
            output = csv.writer(_out)
            for line in data:
                for i, item in enumerate(line):
                    try:
                        date_time = dt.datetime.strptime(item.strip(), format_)
                        quoted_dt = "'{0}'".format(date_time.strftime(gtnp_date_time_format))
                        line[i] = quoted_dt
                    except ValueError as error:
                        print(error, file=_log)
                output.writerow(line)
        OUTFILE_OUT.send(outfile)
        LOGFILE_OUT.send(logfile)
    # date_time_writer = csv.writer(open(out_file, 'wb'), lineterminator='\n')
    # with open(column_file, 'rb') as csvfile:
    #     date_time_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    #     for row in date_time_reader:
    #         try:
    #             date_time = dt.datetime.strptime(row[0].strip(), in_format)
    #             quoted_dt = "{0}".format(date_time.strftime(gtnp_date_time_format))
    #             date_time_writer.writerow([quoted_dt])
    #         except ValueError as error:
    #             print(error)
    #             date_time_writer.writerow(row)
