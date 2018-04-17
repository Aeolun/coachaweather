from django.urls import path, include
from .views import map_list, map_step, map_detail, map_base, map_tiles

urlpatterns = [
    path('basemap', map_base),
    path('map', map_list),
    path('map/<int:pk>', map_detail),
    path('map/<int:pk>/tiles', map_tiles),
    path('map/<int:pk>/step', map_step)
]