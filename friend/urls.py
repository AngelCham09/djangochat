from django.urls import path

from . import views

urlpatterns = [
    path('', views.friends, name='friends'),
    path('friend_request/', views.send_friend_request, name='friend-request'),
    path('accept_friend_request/', views.accept_friend_request, name='accept-friend-request'),
    path('reject_friend_request/', views.reject_friend_request, name='reject-friend-request'),
    path('unfriend_request/', views.unfriend_request, name='unfriend-request'),
    path('cancel_friend_request/', views.cancel_friend_request, name='cancel-friend-request'),
]