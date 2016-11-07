#! /usr/bin/python
import re
import csv

import rill


@rill.component
@rill.inport('INFILE')
@rill.inport('OUTFILE')
@rill.outport('OUTFILE_OUT')
def minsec_to_decimal(INFILE, OUTFILE, OUTFILE_OUT):
    """Convert lat/long coordinates from minutes and seconds to decimal."""
    for infile, outfile in zip(INFILE.iter_contents(), OUTFILE.iter_contents()):
        with open(infile, newline='') as _in, open(outfile, 'w', newline='') as _out:
            data = csv.reader(_in)  # Set ingest settings here, we may want to ignore the comma in the original string
            output = csv.writer(_out)
            for coord in data:
                # Splits each coordinate pair into degrees, minutes, seconds, and
                # hemisphere marker.
                coord = ','.join(coord)
                coord = coord.upper()
                subs = re.split(r'\s*[\xb0"\',]\s*|.(?=[NESW])|(?<=[NESW]).|\n', coord)
                subs = [_f for _f in subs if _f]

                names = ['degrees', 'minutes', 'seconds']
                values = {name: 0 for name in names}
                pair = [0, 0]
                for (which, section) in enumerate([subs[:len(subs) / 2],
                                                   subs[len(subs) / 2:]]):
                    # Assumes that the format of the input is symmetric
                    # e.g. you won't have degrees-minutes-seconds North and only degrees East
                    sign = 1
                    for (i, elem) in enumerate(section):
                        if (elem in 'NESW'):
                            sign = -1 if elem in 'SW' else 1
                        else:
                            values[names[i]] = float(elem)
                    pair[which] = (values['degrees'] + values['minutes'] / 60
                                   + values['seconds'] / 3600) * sign
                output.writerow(pair)


#     data = io.pull(infile, str)
#
#     out = []
    # for coord in data:
    #     # Splits each coordinate pair into degrees, minutes, seconds, and
    #     # hemisphere marker.
    #     coord = ','.join(coord)
    #     coord = coord.upper()
    #     subs = re.split(r'\s*[\xb0"\',]\s*|.(?=[NESW])|(?<=[NESW]).|\n', coord)
    #     subs = [_f for _f in subs if _f]
    #
    #     names = ['degrees', 'minutes', 'seconds']
    #     values = dict([(name, 0) for name in names])
    #     pair = [0, 0]
    #     for (which, section) in enumerate([subs[:len(subs) / 2],
    #                                        subs[len(subs) / 2:]]):
    #         sign = 1
    #         for (i, elem) in enumerate(section):
    #             if (elem in 'NESW'):
    #                 sign = -1 if elem in 'SW' else 1
    #             else:
    #                 values[names[i]] = float(elem)
    #         pair[which] = (values['degrees'] + values['minutes'] / 60
    #                        + values['seconds'] / 3600) * sign
    #     out.append(pair)
#
#     io.push(interpret_out(out), outfile)
#
#
# def interpret_out(data):
#     out = []
#     for line in data:
#         out.append('{0:2.7f}, {1:3.7f}'.format(line[0], line[1]))
#     return out
