__author__ = 'alex'

from django import forms
from ckeditor.widgets import CKEditorWidget

from pythonizame.apps.blog.models import LikePost, FavoritePost, Post


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget)

    class Meta:
        model = Post
        exclude = ['author', 'slug', 'timestamp', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'main_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'pin_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'author_image': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': "Nombre del autor, ejemplo 'Gaspar Dzul - Flickr'"}),
            'author_link': forms.URLInput(attrs={'class': 'form-control'}),
            'abstract': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': "Título",
            'main_image': "Imagen principal.",
            'pin_image': "Imagen pequeña.",
            'author_image': "Autor de la imagen.",
            'author_link': "Link del autor.",
            'abstract': "Texto de introducción.",
            'content': "Contenido de la publicación",
            'category': "Categoría",
        }
        help_texts = {
            'main_image': "Imagen de portada de la publicación",
            'pin_image': "Imagen que se visualiza en el listado de las publicaciones",
            'author_image': "Se recomienda que el autor de ambas imagenes sea el mismo.",
            'abstract': "Máximo 200 caracteres",
        }


class LikeForm(forms.ModelForm):
    class Meta:
        model = LikePost
        exclude = ['created_by', 'timestamp']


class FavoriteForm(forms.ModelForm):
    class Meta:
        model = FavoritePost
        exclude = ['created_by', 'timestamp']
