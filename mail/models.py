from django.db import models
from account.models import User


# Create your models here.
class Mail(models.Model):
    to_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='to_users')
    from_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='from_users')
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
