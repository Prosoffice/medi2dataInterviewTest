import django_filters
from .models import Patient


class PatientFilter(django_filters.FilterSet):
    appointment = django_filters.DateFilter(
        field_name='appointment__start_time',
        lookup_expr='date',  # Filter by date part only
    )

    surgeries = django_filters.CharFilter(
        field_name='record__surgeries',
        lookup_expr='icontains',
    )

    class Meta:
        model = Patient
        fields = ['appointment', 'surgeries']
