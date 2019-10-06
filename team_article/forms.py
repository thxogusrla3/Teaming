from django import forms
from .models import ArticleFile, ArticleUrl

# file_url = models.FileField(upload_to=article_file_path)
# image_url = models.FileField(upload_to=article_image_path)
# url = models.URLField(max_length=300)

class ArticleFileForm(forms.ModelForm):
    class Meta:
        model = ArticleFile
        fields = ['file_url','explain_content']


class ArticleUrlForm(forms.ModelForm):
    class Meta:
        model = ArticleUrl
        fields = ['url','explain_content']