from django import forms
from .models import Post
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

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


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user