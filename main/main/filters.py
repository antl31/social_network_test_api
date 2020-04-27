import django_filters
from .models import PostLike


class ShellMessageFilter(django_filters.FilterSet):
    date_from = django_filters.DateTimeFilter(lookup_expr="gte")
    date_to = django_filters.DateTimeFilter(lookup_expr='lte')

    class Meta:
        model = PostLike
        fields = ['last_updated']
