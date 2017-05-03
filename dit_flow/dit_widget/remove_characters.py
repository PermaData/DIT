import re
import csv

from circuits import Component

class RemoveCharacters(Component):

    channel = 'RemoveCharacters'

    def go(self, event):
        print(self.channel, ' received go event')

def remove_characters(INFILE, OUTFILE_IN, CHARACTERS, LOGFILE_IN, OUTFILE_OUT, LOGFILE_OUT):
    """Remove all from a set of characters from a column.

    Input:
        chars:
        substring: If False (the default), chars is interpreted as a set
            of individual characters. If True, chars is interpreted as a
            defined substring, and this works like search and replace.
        placeholder: If '' (the default), the characters are removed.
            If another string, every character in chars is replaced by
            placeholder.
    """
    # These used to be optional arguments and may become that again if that is
    # possible within rill
    substring = False
    placeholder = ''
    for infile, outfile, charset, logfile in zip(INFILE.iter_contents(),
                                        OUTFILE_IN.iter_contents(),
                                        CHARACTERS.iter_contents(),
                                        LOGFILE_IN.iter_contents()):
        for chars in charset:
            if (substring):
                # Treat chars as a strict substring
                target = re.escape(chars)
            else:
                # Treat chars as individual characters
                target = '[' + re.escape(chars) + ']'
            with open(infile, newline='') as _in, \
                 open(outfile, 'w', newline='') as _out, \
                 open(logfile, 'a') as _log:
                data = csv.reader(_in)
                output = csv.writer(_out)
                for line in data:
                    modified = line
                    for i, item in enumerate(line):
                        modified[i] = re.sub(target, placeholder, item).strip()
                    output.writerow(modified)

            OUTFILE_OUT.send(outfile)
            LOGFILE_OUT.send(logfile)
