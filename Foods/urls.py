from django.urls import path
from . import views
urlpatterns = [
    path('foodtypes',views.FoodTypes),
    path('fooditems',views.FoodItems),
    path('place_order',views.place_order)
]
