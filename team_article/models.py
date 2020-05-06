from django.db import models
from team.models import Team
from account.models import User
import os

def article_file_name(fileUrl):
    a = 0
    for i in range(len(fileUrl)):
        if fileUrl[i] == '/':
            a = i
    return a

# Create your models here.
def article_file_path(instance, filename):
    return 'articlefile/{}/{}/files/{}'.format(instance.team.team_name, instance.user.username, filename)


def article_image_path(instance, filename):
    return 'articles/{}/images/{}'.format(instance.article.pk, filename)


def comment_file_path(instance, filename):
    return 'articles/{}/comment/{}/files/{}'.format(instance.comment.article.pk, instance.comment.pk, filename)


def comment_image_path(instance, filename):
    return 'articles/{}/comment/{}/images/{}'.format(instance.comment.article.pk, instance.comment.pk, filename)



class ArticleFile(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_url = models.FileField(upload_to=article_file_path)
    explain_content = models.CharField(max_length=300)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now=True)

    def summary(self):
        return self.file_url.name[article_file_name(self.file_url.name)+1:]
    
    def __str__(self):
        return self.explain_content
    
class ArticleUrl(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField(max_length=300)
    explain_content = models.CharField(max_length=300)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.explain_content

    def summary(self):
        return self.url[0:25]
    
class CommentUrl(models.Model):
    articleurl = models.ForeignKey(ArticleUrl, on_delete=models.CASCADE)
    post_user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

class CommentFile(models.Model):
    articlefile = models.ForeignKey(ArticleFile, on_delete=models.CASCADE)
    post_user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content


# class ArticleImage(models.Model):
#     article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='images')
#     image_url = models.FileField(upload_to=article_image_path)
#     explain_content = models.CharField(max_length=300)
#     created_date = models.DateTimeField(auto_now_add=True, editable=False)
#     modified_date = models.DateTimeField(auto_now=True)
