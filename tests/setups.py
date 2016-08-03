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
    with open('Numerics.in', 'w') as f:
        f.write(contents)
        f.close()
    return 'Numerics.in'
    
    
def setup_latlong():
    contents = '''32\xb0 18' 23.1" N, 122\xb0 36' 52.5" W
32\xb0 18.385' N, 122\xb0 36.875' W
32.30642\xb0 N, 122.61458\xb0 W
+32.30642, -122.61458'''
    with open('Latlong_formats.in', 'w') as f:
        f.write(contents)
    return 'Latlong_formats.in'