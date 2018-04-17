from ..models import Map
from django.forms.models import model_to_dict
import random

class Processor():
    def __init__(self, map: Map):
        self.map = map
        self.tiles = self.retrieve_tiles(map)
        self.new_tiles = None

        self.temperature = 0
        self.wind_direction = 0
        self.wind_speed = 0

    def retrieve_tiles(self, map: Map):
        tiles = []
        for tile in map.tiles.all():
            try:
                exists = tiles[tile.x]
            except:
                tiles.insert(tile.x, [])
            tiles[tile.x].insert(tile.y, tile)

        return tiles

    def new_step(self):
        tiles = []
        for row in self.tiles:
            for tile in row:
                try:
                    exists = tiles[tile.x]
                except:
                    tiles.insert(tile.x, [])
                tiles[tile.x].insert(tile.y, model_to_dict(tile))

        return tiles

    def save_tiles(self):
        for row in self.new_tiles:
            for tileinfo in row:
                tile = self.tiles[tileinfo['x']][tileinfo['y']]
                tile.current_water = tileinfo['current_water']
                tile.current_rain = tileinfo['current_rain']
                tile.current_ice = tileinfo['current_ice']
                tile.current_low_clouds = tileinfo['current_low_clouds']
                tile.current_high_clouds = tileinfo['current_high_clouds']

                tile.save()

    def initialize(self, temperature, wind_speed, wind_direction):
        self.new_tiles = self.new_step()
        self.temperature = int(temperature)
        self.wind_speed = int(wind_speed)
        self.wind_direction = int(wind_direction)

    def step(self, temperature, wind_speed, wind_direction):
        self.initialize(temperature, wind_speed, wind_direction)

        for row in self.tiles:
            for tile in row:
                self.wind(tile)
                self.evaporation(tile)
                self.rain(tile)
                self.melting(tile)
                self.freezing(tile)
                self.water(tile)

        self.save_tiles()

    def evaporation(self, tile, always=False):
        adjusted_temp = self.get_adjusted_temperature(tile.elevation)
        if adjusted_temp > 15 and tile.elevation <= 10:
            if random.randint(0, 5) >= 4 or always:
                self.__adjust_tile_value(tile, 'current_low_clouds', random.randint(1, int(adjusted_temp)))

    def wind(self, tile):
        if tile.current_low_clouds > 0 and self.wind_speed > 0:
            (xdiff, ydiff) = self.__get_wind_vector()
            for i in range(0, self.wind_speed):
                modtile = self.get_tile(tile, xdiff * self.wind_speed, ydiff * self.wind_speed)
                if modtile:
                    self.__adjust_tile_value(modtile, 'current_low_clouds', tile.current_low_clouds / self.wind_speed)
            self.__adjust_tile_value(tile, 'current_low_clouds', -tile.current_low_clouds)

    def rain(self, tile):
        adjusted_temp = self.get_adjusted_temperature(tile.elevation)
        if adjusted_temp < 10 and tile.current_low_clouds >= 5:
            self.__adjust_tile_value(tile, 'current_rain', 5)
            self.__adjust_tile_value(tile, 'current_low_clouds', -5)
        # if tile.current_rain > 0 and tile.current_low_clouds <= 0:
        #     self.adjust_tile_value(tile, 'current_rain', -tile.current_rain)

    def melting(self, tile):
        adjusted_temp = self.get_adjusted_temperature(tile.elevation)
        if adjusted_temp > 1 and tile.current_ice > 0:
            self.__adjust_tile_value(tile, 'current_ice', -1)
            self.__adjust_tile_value(tile, 'current_water', 1)

    def freezing(self, tile):
        adjusted_temp = self.get_adjusted_temperature(tile.elevation)
        if adjusted_temp < 1 and tile.current_water > 0:
            self.__adjust_tile_value(tile, 'current_water', -1)
            self.__adjust_tile_value(tile, 'current_ice', 1)

    def water(self, tile):
        if tile.current_rain >= 2:
            self.__adjust_tile_value(tile, 'current_rain', -2)
            self.__adjust_tile_value(tile, 'current_water', 5)
        if tile.current_water > 0:
            lowesttile = self.__get_lowest_surrounding_tile(tile)
            self.__adjust_tile_value(lowesttile, 'current_water', tile.current_water / 2)
            self.__adjust_tile_value(tile, 'current_water', -tile.current_water / 2)
        if tile.current_water > 0 and tile.elevation <= 10:
            self.__adjust_tile_value(tile, 'current_water', -tile.current_water)

    def get_tile(self, currentTile, xdiff, ydiff):
        try:
            return self.tiles[currentTile.x + xdiff][currentTile.y + ydiff]
        except:
            return None

    def __get_lowest_surrounding_tile(self, currentTile):
        lowest = None
        for i in range(-1, 2):
            for j in range(-1, 2):
                tile = self.get_tile(currentTile, i, j)
                if tile != None and (lowest == None or tile.elevation < lowest.elevation):
                    lowest = tile

        return lowest

    def __get_wind_vector(self):
        if self.wind_direction == 0:
            return (-1, 0)
        elif self.wind_direction == 1:
            return (-1, 1)
        elif self.wind_direction == 2:
            return (0, 1)
        elif self.wind_direction == 3:
            return (1, 1)
        elif self.wind_direction == 4:
            return (1, 0)
        elif self.wind_direction == 5:
            return (1, -1)
        elif self.wind_direction == 6:
            return (0, -1)
        elif self.wind_direction == 7:
            return (-1, -1)

    def __adjust_tile_value(self, tile, value, change):
        self.new_tiles[tile.x][tile.y][value] += change

    def get_adjusted_temperature(self, elevation):
        return int(self.temperature) - (elevation / 3)
