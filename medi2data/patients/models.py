from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class Patient(BaseModel):
    """
            Represents a Patient
    """

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    contact_information = models.CharField(max_length=100)


class MedicalRecord(BaseModel):
    """
        Represents a patient's medical record, Sensitive fields are encrypted
    """
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="record")
    allergies = models.TextField(blank=True, null=True)
    medications = models.TextField(blank=True, null=True)
    previous_illnesses = models.TextField(blank=True, null=True)
    surgeries = models.TextField(blank=True, null=True)
