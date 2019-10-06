from django.urls import path
from . import views
app_name = 'team'
urlpatterns = [
    path('create_team/<int:team_pk>/',views.create_team, name='create_team'),
    path('<int:team_id>/<int:user_id>/', views.detail_team, name="detail_team"),
    path('<int:team_id>/<int:user_id>', views.add_member,name="add_member"),
    path('<int:team_id>/<int:user_id>/expulsion_member/', views.expulsion_member, name="expulsion_member"),
    # path('<int:team_id>/<int:user_id>/team_delete/', views.team_delete, name="team_delete"),
    # path('<int:team_id>', views.correct_team, name="correct_team"),
    path('<int:team_id>/<int:user_id>/leave_team/',views.leave_team, name='leave_team'),
    path('<int:team_pk>/edit_team/', views.edit_team, name='edit_team'),
]