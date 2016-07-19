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
        leap = leap_year(year)
        month = t.tm_month
        mid_day = month_days[leap][month-1] / 2
        hour = mid_day % 1 * 24
        
        
        
def leap_year(year):
    if (year%4 == 0):
        if (year%100 == 0):
            if (year%400 == 0):
                return True
            return False
        return True
    return False