import time

import common.readwrite as io
import common.parseargs as pa


def mid_month(infile, outfile, format):
    dates = io.pull(infile, str)
    
    month_days = [[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],  # Not leap year
                  [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],  # Is leap year
                  ]
    
    out = []
    for date in dates:
        t = time.strptime(format, date)
        year = t.tm_year
        leap = leap_year(year)
        month = t.tm_month
        mid_day = month_days[leap][month-1] / 2
        hour = mid_day % 1 * 24
        
        outputdate = (year, month, day, hour, 0, 0, 0, 0, -1)
        
        out.append(time.strftime('%Y-%m-%d %H:%M', outputdate))
        
    io.push(out, outfile)
        
def leap_year(year):
    if (year%4 == 0):
        if (year%100 == 0):
            if (year%400 == 0):
                return True
            return False
        return True
    return False
    
    
# def doy(month, day, leap, month_days):
    # count = 0
    # for i in range(month-1):
        # count += month_days[leap][month-1]
    # count += day
    # return count
    
    
#                 PERFORM FUNCTION USING COMMAND-LINE OPTIONS                 #
args = pa.parse_args(sys.argv[1:])
infile = args[0]
outfile = args[1]
format = args[3][0]

mid_month(infile, outfile, format)