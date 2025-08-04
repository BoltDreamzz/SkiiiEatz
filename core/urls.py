from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('restaurants/<slug:slug>/', views.restaurant_detail, name='restaurant_detail'),
    path('explore/', views.explore, name='explore'),
    path('get-location-data/', views.get_location_data, name='get_location_data'),
    path('get-city-data/', views.general_search, name='general_search'),
    path('all-restaurants/', views.all_restaurants, name='all_restaurants'),
    path('all-supermarkets/', views.all_supermarkets, name='all_supermarkets'),
    path('', views.view_cart, name='view_cart'),
    path('add-menu-item/<int:restaurant_id>/<int:item_id>/', views.add_menu_item_to_cart, name='add_menu_item_to_cart'),
    path('delete-pack/<int:pack_id>/', views.delete_pack, name='delete_pack'),
]
