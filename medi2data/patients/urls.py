from django.urls import path
from . import views

urlpatterns = [
    path('', views.PatientListCreateView.as_view(), name='patient-list-create'),
    path('<int:pk>/', views.PatientDetailView.as_view(), name='patient-detail-delete-update'),
    path('<int:patient_id>/medical-records/', views.MedicalRecordListCreateView.as_view(), name='medical-record-list'
                                                                                                '-create'),
    path('medical-record/<int:pk>/', views.MedicalRecordUpdateView.as_view(), name='medical-record-detail-delete'
                                                                                    '-update'),
]
