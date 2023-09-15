from django_filters import FilterSet, DateFilter, ModelChoiceFilter
from .models import Post, Category
from .forms import SingleDateWidget


class PostFilter(FilterSet):
    date_after = DateFilter(field_name='date_of_creation_post', lookup_expr='date__gt', widget=SingleDateWidget)
    category_name = ModelChoiceFilter(
        field_name='postcategory__categories_id',
        queryset=Category.objects.all(),
        label='Category',
    )

    class Meta:
       model = Post
       fields = {
           'author__name_author': ['exact'],
           'title_post': ['icontains'],
       }


