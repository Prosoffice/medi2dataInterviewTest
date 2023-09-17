from django.db import models
from django.utils import timezone
from patients.models import BaseModel, Patient


class Appointment(BaseModel):
    """
            Represents a appointment instance for patients
    """
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointment")
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    description = models.TextField()
