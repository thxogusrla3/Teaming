from django import forms
from .models import ArticleFile, ArticleUrl

# file_url = models.FileField(upload_to=article_file_path)
# image_url = models.FileField(upload_to=article_image_path)
# url = models.URLField(max_length=300)

class ArticleFileForm(forms.ModelForm):
    class Meta:
        model = ArticleFile
        fields = ['file_url','explain_content']
        widgets = {
            'file_url':forms.FileInput(attrs={'class':'form-control','placeholder': 'file_url'}),
            'explain_content':forms.TextInput(attrs={'class':'form-control', 'placeholder': 'explain_content'})
        }
        labels = {
            'file_url':'파일',
            'explain_content':'파일 설명'
        }

class ArticleUrlForm(forms.ModelForm):
    class Meta:
        model = ArticleUrl
        fields = ['url','explain_content']
        widgets = {
            'url':forms.TextInput(attrs={'class':'form-control', 'placeholder':'url'}),
            'explain_content':forms.TextInput(attrs={'class':'form-control', 'placeholder':'explain_content'})
        }
        labels = {
            'url':'주소',
            'explain_content':'주소 설명'
        }