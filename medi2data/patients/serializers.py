from rest_framework import serializers
from .models import Patient, MedicalRecord


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class PatientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

    name = serializers.CharField(required=False)
    date_of_birth = serializers.DateField(required=False)
    gender = serializers.ChoiceField(choices=Patient.GENDER_CHOICES, required=False)
    contact_information = serializers.CharField(required=False)


class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = '__all__'


class MedicalRecordUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = '__all__'

    patient = serializers.CharField(required=False)
    allergies = serializers.CharField(required=False)
    medications = serializers.CharField(required=False)
    previous_illnesses = serializers.CharField(required=False)
    surgeries = serializers.CharField(required=False)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['patient'] = instance.patient_id  # Replace 'patient' with 'patient_id'
        return representation
