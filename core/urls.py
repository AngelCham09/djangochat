from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

urlpatterns = [
    path('', views.frontpage, name='frontpage'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('profile/', views.profile, name='profile'),
    path('profile/change_pwd/', views.CustomPasswordChangeView.as_view(), name='changePwd'),
    path('profile/my_friend/', views.my_friend, name='myFriend'),
    path('profile/friend_request/', views.friend_request, name='friendRequest'),
]