from django.shortcuts import render
import json
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.crypto import get_random_string
from .weather_control.processing import Processor
from .models import Map, Tile, CurrentTile

# Create your views here.
@require_http_methods(["POST"])
def map_base(request):
    jsondata = json.loads(request.POST["data"])

    for rowdata in jsondata:
        for tiledata in rowdata:
            (tile, created) = Tile.objects.get_or_create(x=tiledata['x'], y=tiledata['y'], defaults={
                'elevation': 0,
                'base_water': 0,
                'base_ice': 0
            })
            tile.x = tiledata['x']
            tile.y = tiledata['y']
            tile.elevation = tiledata['elevation']
            tile.base_water = tiledata['current_water']
            tile.base_ice = tiledata['current_ice']

            tile.save()

    return JsonResponse({ 'success': True })

@require_http_methods(["POST"])
def map_list(request):
    map = Map()
    map.name = get_random_string(length=32)
    map.save()

    for tile in Tile.objects.all():
        current_tile = CurrentTile()
        current_tile.x = tile.x
        current_tile.y = tile.y
        current_tile.elevation = tile.elevation
        current_tile.current_water = tile.base_water
        current_tile.current_ice = tile.base_ice
        current_tile.current_high_clouds = 0
        current_tile.current_low_clouds = 0
        current_tile.current_rain = 0

        current_tile.map = map
        current_tile.save()

    return JsonResponse(model_to_dict(map))

@require_http_methods(["GET"])
def map_detail(request, pk):
    map = Map.objects.get(pk=pk)

    return JsonResponse(map)

@require_http_methods(["GET"])
def map_tiles(request, pk):
    map = Map.objects.get(pk=pk)

    tiles = []
    for tile in map.tiles.all():
        try:
            exists = tiles[tile.x]
        except:
            tiles.insert(tile.x, [])
        tiles[tile.x].insert(tile.y, model_to_dict(tile))


    return JsonResponse(tiles, safe=False)

@require_http_methods(["POST"])
def map_step(request, pk):
    map = Map.objects.get(pk=pk)

    processor = Processor(map)
    processor.step(request.POST['temperature'], request.POST['wind_speed'], request.POST['wind_direction'])

    return JsonResponse(processor.new_tiles, safe=False)