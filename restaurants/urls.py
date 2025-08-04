from django.urls import path
from . import views

app_name = 'restaurants'

urlpatterns = [
    # path('', views.homepage, name='homepage'),
    path('restaurant/<int:pk>/status/', views.restaurant_status_partial, name='restaurant-status-partial'),
]
