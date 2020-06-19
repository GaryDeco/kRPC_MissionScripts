'''Various Helper Methods'''

import krpc
import time

def kerbal_time(secs):
    '''Converts kerbal time into human-readable time (seconds to yr,m,d,h,m,s... :) )'''
    year = int(round(secs) / 7689600)
    day = int(round(secs) / 21600)
    hh = int((round(secs) % 21600) / 3600)
    mm = int((round(secs) % 3600) / 60)
    ss = int(round(secs) % 60)
    ts = "T+%1i.%02i %02i:%02i:%02i" % (year, day, hh, mm, ss)
    return ts
