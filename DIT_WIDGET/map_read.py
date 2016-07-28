import sys

import netCDF4 as nc

import common.readwrite as io
import common.definitions as d

__all__ = ['map_read']


def map_read(infile, outfile, lat_i, long_i, grid, grid_config, grid_meaning):
    """
    Inputs:
        infile: The input csv file with the location data
        outfile: The file to print processed data to
        lat_i: column index of latitudes in infile
        long_i: column index of longitudes in infile
        grid: The file mapping grid position -> information
        grid_config: The file mapping grid type -> information about
            reading it
        grid_meaning: The file mapping information -> useful formats
    """
    with open(infile, 'rb') as fi:
        with open(outfile, 'wb') as fo:
            data = csv.reader(fi)
            push = csv.writer(fo)

            for line in data:
                lon = line[long_i]
                lat = line[lat_i]


def locate_grid(grid, lat, long):


def get_config(grid_config, name):
    """Read the grid_config file to get information for reading.
    Inputs:
        grid_config: name of config file.
        name: Name of grid entry to use
    """
    with open(grid_config) as f:
        target = "'" + name.strip("'") + "'"
        for line in f:
            if (line.startswith(target)):
                subs = line.split()
                if (subs[1] != "'lat_lon'"):
                    raise RuntimeError('Type must be lat_lon')
                return tuple(subs[2:])
    raise RuntimeError('The grid name {0} was not found in file {1}.'.format(
        name, grid_config))


def get_meaning(grid_meaning, number):
    """Read grid_meaning to get useful information out.
    Inputs:
        grid_meaning: Name of mapping file.
        number: Type identifier. Does not actually need to be a number.
    """
    with open(grid_meaning) as f:
        for line in f:
            if line.startswith(number):
                return line.split()[1]
    raise RuntimeError('The type number {0} was not found in file {1}.'.format(
        name, grid_meaning))


class ConfigData:
    def __init__(self, config)
        self.min_lon = config[0]
        self.min_lat = config[1]
        self.width_lon = config[2]
        self.width_lat = config[3]
        self.offset_lon = config[4]
        self.offset_lat = config[5]
        self.num_lon = config[6]
        self.num_lat = config[7]
        
    def locate_grid(self, grid, lat, long):
        ind_lat = (lat - self.min_lat)//self.width_lat
        ind_lon = (long - self.min_lon)//self.width_lon
        if (ind_lat < 0 or ind_lat > self.num_lat or
            ind_lon < 0 or ind_lon > self.num_lon):
            raise IndexError('Coordinate not in grid')
        data = nc.Dataset(grid)
        array = data.get_variables_by_attributes(type='grid')
        
        
        

#                 PERFORM FUNCTION USING COMMAND-LINE OPTIONS                 #
if (__name__ == '__main__'):
    args = parse_args(sys.argv[1:])

    map_read(*args)
