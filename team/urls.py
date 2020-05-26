from django.urls import path
from . import views
app_name = 'team'
urlpatterns = [
    path('create_team/',views.create_team, name='create_team'),
    path('<int:team_id>/', views.detail_team, name="detail_team"),
    path('<int:team_id>/addmember', views.add_member,name="add_member"),
    path('<int:team_id>/<int:user_id>/expulsion_member/', views.expulsion_member, name="expulsion_member"),
    path('<int:team_pk>/<int:user_pk>/leave_team/',views.leave_team, name='leave_team'),
    path('<int:team_pk>/edit_team/', views.edit_team, name='edit_team'),
    path('<int:team_pk>/add_time_table', views.add_time_table, name='add_time_table'),
    path('<int:team_pk>/add_member1', views.add_member1, name='add_member1'),
    path('<int:team_pk>/delete_time_table', views.delete_time_table, name='delete_time_table'),
    path('<int:team_pk>/member_time_table', views.team_user_timetable, name='member_time_table'),
    path('team_meeting_place/', views.team_meeting_place, name='team_meeting_place'),
    path('<int:team_pk>/all_team_member', views.all_team_member, name="all_team_member"),
    path('<int:team_pk>/team_chat', views.team_chat, name="team_chat"),
    path('<int:team_pk>/team_chat_delete', views.team_chat_delete, name="team_chat_delete"),
    
]