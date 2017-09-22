#!/usr/bin/env python3
# coding: utf-8


def integrated_hrs(start, end):
    """
    Calculated integrated hours the compressor has been running
    over the time frame provided.
    """
    conDB = mdb.connect(CONN_PARAMS[0],CONN_PARAMS[1],CONN_PARAMS[2],CONN_PARAMS[3],port=CONN_PARAMS[4])
    cursor = conDB.cursor()
    queryStr = ("SELECT * FROM ThermostatLog BETWEEN {} AND {}".format(start,end))
    cursor.execute(queryStr)
    states = cursor.fetchall()

    total_time = 0
    for i, state in enumerate(states):
        cool = state[4]
        heat = state[5]

        last_cool = states[i-1][4]
        last_heat = states[i-1][5]

        # start
        if (cool == 1 or heat == 1) and (last_cool == 0 and last_heat == 0):
            start = state[0]

        # end
        if (cool == 0 or heat == 0) and (last_cool == 1 and last_heat == 1):
            end = state[0]
            total_time += end - start

    cursor.close()
    conDB.close()

    return total_time