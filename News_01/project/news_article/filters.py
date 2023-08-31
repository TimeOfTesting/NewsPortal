from django_filters import FilterSet, DateFilter
from .models import Post
from .forms import SingleDateWidget


class PostFilter(FilterSet):
    date_after = DateFilter(field_name='date_of_creation_post', lookup_expr='date__gt', widget=SingleDateWidget)

    class Meta:
       model = Post
       fields = {
           'author__name_author': ['exact'],
           'title_post': ['icontains'],
       }



