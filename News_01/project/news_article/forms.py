from django import forms
from .models import Post

class SingleDateWidget(forms.DateInput):
    input_type = 'date'

class PostFormNews(forms.ModelForm):
    class Meta:
        model = Post

        exclude = ['post_type']
        labels = {
            'title_post': 'Заголовок',
            'text_post': 'Текст',
            'rating_post': 'Рейтинг',
            'category': 'Категория',
            'author': "Автор"
        }

