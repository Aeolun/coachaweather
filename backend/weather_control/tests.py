from django.test import TestCase
from .processing import Processor
from django.forms.models import model_to_dict
from ..models import Map, CurrentTile

class ProcessingTestCase(TestCase):
    def __createTile(self, map, x, y, elevation, ice=0, low_clouds=0, high_clouds=0, water=0, rain=0):
        tile = CurrentTile()
        tile.map = map
        tile.x = x
        tile.y = y
        tile.elevation = elevation
        tile.current_ice = ice
        tile.current_low_clouds = low_clouds
        tile.current_high_clouds = high_clouds
        tile.current_water = water
        tile.current_rain = rain
        tile.save()

        return tile

    def __debug(self):
        for tile in self.map.tiles.all():
            print(model_to_dict(tile))

    def setUp(self):
        self.map = Map()
        self.map.save()

        self.tile = self.__createTile(self.map, 0, 0, 10)
        self.tile2 = self.__createTile(self.map, 1, 0, 80)
        self.tile3 = self.__createTile(self.map, 0, 1, 5)
        self.tile4 = self.__createTile(self.map, 1, 1, 15)

        self.map.tiles.add(self.tile)
        self.map.tiles.add(self.tile2)
        self.map.tiles.add(self.tile3)
        self.map.tiles.add(self.tile4)

    def test_new_step(self):
        processor = Processor(self.map)
        tiles = processor.new_step()

        self.assertEqual(self.tile.elevation, tiles[0][0]['elevation'], "Tiles in map and new step are not the same.")
        self.assertEqual(self.tile2.elevation, tiles[1][0]['elevation'], "Tiles in map and new step are not the same.")

    def test_adjusted_temperature(self):
        processor = Processor(self.map)
        processor.initialize(20, 0, 0)

        temp = processor.get_adjusted_temperature(self.tile2.elevation)

        self.assertEqual(-7, round(temp), "Adjusted temperature calculation is not working correctly.")

    def test_evaporation(self):
        processor = Processor(self.map)
        processor.initialize(20, 0, 0)

        processor.evaporation(self.tile3, True)

        self.assertGreater(processor.new_tiles[0][1]['current_low_clouds'], 0, "Evaporation is not working correctly.")

    def test_wind(self):
        self.tile2.current_low_clouds = 10
        self.tile2.save()

        processor = Processor(self.map)
        processor.initialize(20, 1, 0)

        processor.wind(self.tile2)

        self.assertGreater(processor.new_tiles[0][0]['current_low_clouds'], 0, "Wind is not working correctly.")

    def test_rain(self):
        self.tile2.current_low_clouds = 10
        self.tile2.save()

        processor = Processor(self.map)
        processor.initialize(20, 1, 0)

        processor.rain(self.tile2)

        self.assertEqual(5, processor.new_tiles[1][0]['current_low_clouds'], "Rain is not working correctly.")
        self.assertEqual(5, processor.new_tiles[1][0]['current_rain'], "Rain is not working correctly.")

    def test_melting(self):
        self.tile2.current_ice = 10
        self.tile2.save()

        processor = Processor(self.map)
        processor.initialize(60, 0, 0)

        processor.melting(self.tile2)

        self.assertEqual(9, processor.new_tiles[1][0]['current_ice'], "Melting is not working correctly.")
        self.assertEqual(1, processor.new_tiles[1][0]['current_water'], "Melting is not working correctly.")


    def test_freezing(self):
        self.tile2.current_water = 10
        self.tile2.save()

        processor = Processor(self.map)
        processor.initialize(10, 0, 0)

        processor.freezing(self.tile2)

        self.assertEqual(9, processor.new_tiles[1][0]['current_water'], "Freezing is not working correctly.")
        self.assertEqual(1, processor.new_tiles[1][0]['current_ice'], "Freezing is not working correctly.")

    def test_water(self):
        self.tile2.current_water = 10
        self.tile2.save()

        processor = Processor(self.map)
        processor.initialize(10, 0, 0)

        processor.water(self.tile2)

        self.assertEqual(5, processor.new_tiles[1][0]['current_water'], "Water is not working correctly.")
        self.assertEqual(5, processor.new_tiles[0][1]['current_water'], "Water is not working correctly.")

