import time

import common.readwrite as io


def mid_month(infile, outfile):
    dates = io.pull(infile, str)
    
    month_days = [[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
                  [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
                  ]
    
    for date in dates:
        t = time.strptime('%Y-%m-%d %H:%M', date)
        year = t.tm_year
        month = t.tm_month