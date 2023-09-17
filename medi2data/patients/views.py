from rest_framework import generics
from rest_framework import permissions
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PatientFilter
from .models import Patient, MedicalRecord
from .serializers import (PatientSerializer,
                          MedicalRecordSerializer,
                          PatientUpdateSerializer,
                          MedicalRecordUpdateSerializer
                          )


class PatientListCreateView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PatientFilter

    def get_queryset(self):
        queryset = super().get_queryset()

        # Get the search query from the request
        query = self.request.query_params.get('query', '')

        # If a search query is provided, filter the queryset
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(date_of_birth__date=query) |
                Q(appointment__start_time__date=query)
            ).distinct()

        return queryset


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]


class MedicalRecordListCreateView(generics.ListCreateAPIView):
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        patient_id = self.kwargs.get('patient_id')
        return MedicalRecord.objects.filter(patient__id=patient_id)

    def perform_create(self, serializer) -> None:
        patient_id = self.kwargs.get('patient_id')
        patient = Patient.objects.get(id=patient_id)
        serializer.save(patient=patient)


class MedicalRecordUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
