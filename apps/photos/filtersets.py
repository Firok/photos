from django_filters import FilterSet, BooleanFilter
from .models import Photo


class PhotoFilter(FilterSet):

    # Filter for photos if photos are published or not
    published = BooleanFilter(
        field_name='published_at', method='filter_published')

    def filter_published(self, queryset, name, value):
        lookup = '__'.join([name, 'isnull'])
        return queryset.filter(**{lookup: not value})

    class Meta:
        model = Photo
        fields = ['user', 'published']
