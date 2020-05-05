import krpc
import numpy as np
from collections import namedtuple, defaultdict



conn = krpc.connect()
KSC = conn.space_center
vessel = KSC.active_vessel

# call at prelaunch and store values
total_stages = vessel.control.current_stage
all_stages = [i for i in range(0, total_stages)]
this_stage = max(all_stages)
next_stage = this_stage - 1
last_stage = this_stage + 1
remaining_stages = [i for i in range(0, this_stage)]
final_stage = min(all_stages)
mid_stage = [i for i in all_stages if i is not this_stage and i is not final_stage]

def list_stages(arg):
    '''
    **Returns either an integer or a list of integers**
    :params:\n
    - total_stages, all_stages, this_stage, next_stage, last_stage,\n
    - remaining_stages, final_stage, mid_stage
     '''
    total_stages = vessel.control.current_stage
    all_stages = [i for i in range(0, total_stages)]
    this_stage = max(all_stages)
    next_stage = this_stage - 1
    last_stage = this_stage + 1
    remaining_stages = [i for i in range(0, this_stage)]
    final_stage = min(all_stages)
    mid_stage = [i for i in all_stages if i is not this_stage and i is not final_stage]
    return arg

def list_engines(vstage):
    '''**Returns a list of engines in the specified stage**
    :params:\n
     int(stage) or all_stages returns a list of engines in all stages
    '''
    total_stages = vessel.control.current_stage
    all_stages = [i for i in range(0, total_stages)]
    if vstage == all_stages:
        return [i for i in vessel.parts.engines if i.part.engine]
    else:
        return [i for i in vessel.parts.engines if i.part.stage == vstage]

def list_parts(vstage):
    '''**Returns a list of parts in the specified stage**
    :params:\n
    int(stage) or defined stage_variables
    '''
    parts_list = [i for i in vessel.parts.all if i.stage == vstage]
    return parts_list


def kerbal_time(secs):
    '''Converts kerbal time into human-readable time (seconds to yr,m,d,h,m,s... :) )'''
    year = int(round(secs) / 7689600)
    day = int(round(secs) / 21600)
    hh = int((round(secs) % 21600) / 3600)
    mm = int((round(secs) % 3600) / 60)
    ss = int(round(secs) % 60)
    ts = "T+%1i.%02i %02i:%02i:%02i" % (year, day, hh, mm, ss)
    return ts
