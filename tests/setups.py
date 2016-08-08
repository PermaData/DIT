import os

PATH = os.path.abspath('.') + '\\'


"""

NUMERIC PROCESSING
------------------

"""


def setup_numeric():
    """Sets up the proper context for the numeric widgets
    NOTE THAT IT WRITES THE FILE THEN RETURNS THE FILE NAME
    """
    contents = '''3.14233
4.122288
5.233
7.4333355
777.2
-999.000000
777.2'''
    with open(PATH + 'Numerics.in', 'w') as f:
        f.write(contents)
    return PATH + 'Numerics.in'


def setup_statistics():
    contents = '''2
2
3
4
4
-999'''
    with open(PATH + 'Easy_stats.in', 'w') as f:
        f.write(contents)
    return PATH + 'Easy_stats.in'


"""

COORDINATE FORMAT CONVERSION
----------------------------

"""


def setup_minsec():
    contents = '''32\xb0 18' 23.1" N, 122\xb0 36' 52.5" W
32\xb0 18.385' N, 122\xb0 36.875' W
32.30642\xb0 N, 122.61458\xb0 W
+32.30642, -122.61458'''
    # These examples from https://www.maptools.com/tutorials/lat_lon/formats
    with open(PATH + 'Minsec.in', 'w') as f:
        f.write(contents)
    return PATH + 'Minsec.in'


def setup_decimal():
    contents = '''40.0150, -105.2705
48.8566, 2.3522
-6.1630, 35.7516
-22.9068, -43.1729'''
    # Boulder, Paris, Dodoma, Rio de Janeiro
    with open(PATH + 'Decimal.in', 'w') as f:
        f.write(contents)
    return PATH + 'Decimal.in'


"""

COORDINATE CONVERSION
---------------------

"""


def setup_utm_conversion():
    contents = '''ID,E,N,Zone,Elevation,Number of Records,Start Date,End Date
1,621988,6088495,19,644,8,8/15/1977,9/30/1980
2,621900,6089268,19,649,9,10/1/1977,8/30/1980
3,621534,6089464,19,639,8,10/1/1977,8/30/1980
4,621630,6089558,19,655,8,10/1/1977,9/30/1980'''
    with open(PATH + 'UTM_test.in', 'w') as f:
        f.write(contents)
    return PATH + 'UTM_test.in'


def setup_latlong_conversion():
    contents = '''ID,Elevation,Number of Records,Start Date,End Date,Lat,Lon
1,644,8,8/15/1977,9/30/1980,54.92851,-67.096264
2,649,9,10/1/1977,8/30/1980,54.935474,-67.097309
3,639,8,10/1/1977,8/30/1980,54.937324,-67.102935
4,655,8,10/1/1977,9/30/1980,54.938144,-67.101398'''
    with open(PATH + 'LatLong_test.in', 'w') as f:
        f.write(contents)
    return PATH + 'LatLong_test.in'
