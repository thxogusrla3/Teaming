from django.urls import path
from . import views

app_name = 'mail'
urlpatterns = [
    path('mailbox/<int:user_id>/', views.mailbox, name='mailbox'),
    path('send_mail/<int:from_id>/', views.send_mail, name='send_mail'),
    path('delete_mail/<int:mail_id>/', views.delete_mail, name='delete_mail'),
    path('detail_mail/<int:mail_id>/', views.detail_mail, name='detail_mail'),
]