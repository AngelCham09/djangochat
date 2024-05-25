from django.urls import path

from . import views

urlpatterns = [
    path('', views.rooms, name='rooms'),
    path('add/', views.addRooms, name='addRooms'),
    path('<slug:slug>/', views.room, name='room'),
    path('api/images/', views.ChatImageApiView.as_view(), name='room_images'),
]