from django_filters import FilterSet,DateFilter
from .models import PostLike


class DateFilter(FilterSet):
    date_to = DateFilter(field_name='last_updated', lookup_expr='lte', )
    date_from = DateFilter(field_name='last_updated', lookup_expr='gte')

    class Meta:
        model = PostLike
        fields = ['last_updated']
