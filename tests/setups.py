import os

PATH = os.path.abspath('.') + '\\'


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






def setup_latlong():
    contents = '''32\xb0 18' 23.1" N, 122\xb0 36' 52.5" W
32\xb0 18.385' N, 122\xb0 36.875' W
32.30642\xb0 N, 122.61458\xb0 W
+32.30642, -122.61458'''
    with open(PATH + 'Latlong_formats.in', 'w') as f:
        f.write(contents)
    return PATH + 'Latlong_formats.in'









def setup_utm_conversion():
    contents = '''ID,E,N,Zone,Elevation,Number of Records,Start Date,End Date
1,621988,6088495,19,644,8,8/15/1977,9/30/1980
2,621900,6089268,19,649,9,10/1/1977,8/30/1980
3,621534,6089464,19,639,8,10/1/1977,8/30/1980
4,621630,6089558,19,655,8,10/1/1977,9/30/1980
5,621764,6089263,19,641,4,10/1/1977,2/26/1980
6,621760,6089389,19,651,9,10/1/1977,8/30/1980
7,621264,6090266,19,616,6,7/22/1979,9/30/1980
8,621335,6090164,19,621,6,7/22/1979,9/30/1980
9,622343,6088804,19,631,5,7/20/1977,8/31/1979'''
    with open(PATH + 'UTM_test.in', 'w') as f:
        f.write(contents)
    return PATH + 'UTM_test.in'


def setup_latlong_conversion():
    # Note: this was the output from utm_to_latlong
    contents = '''ID,Elevation,Number of Records,Start Date,End Date,Lat,Lon
1,644,8,8/15/1977,9/30/1980,54.9285096341267,-67.09626403013718
2,649,9,10/1/1977,8/30/1980,54.935473877492164,-67.09730870702437
3,639,8,10/1/1977,8/30/1980,54.93732351866916,-67.10293508242019
4,655,8,10/1/1977,9/30/1980,54.93814440147724,-67.10139771396229
5,641,4,10/1/1977,2/26/1980,54.93546216489981,-67.0994322973866
6,651,9,10/1/1977,8/30/1980,54.936594818434216,-67.09944130955579
7,616,6,7/22/1979,9/30/1980,54.944592435540876,-67.10680852559405
8,621,6,7/22/1979,9/30/1980,54.943659053415374,-67.10574382386544
9,631,5,7/20/1977,8/31/1979,54.931198063772904,-67.09059585078842'''
    with open(PATH + 'LatLong_test.in', 'w') as f:
        f.write(contents)
    return PATH + 'LatLong_test.in'