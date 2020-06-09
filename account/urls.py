from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('sign_up/', views.sign_up, name='sign_up'),
    path('', views.sign_in, name='sign_in'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('edit_user/', views.edit_user, name='edit_user'),
    path('user_home/<int:user_pk>', views.user_home, name='user_home'),
    path('user_info/<int:user_pk>', views.user_info, name='user_info'),
    path('schedule/', views.set_schedule, name='set_schedule'),
    path('user_team/<int:user_pk>', views.user_team, name='user_team'),
    path('overlap_username/',views.overlap_username, name="overlap_username"),
    
]
