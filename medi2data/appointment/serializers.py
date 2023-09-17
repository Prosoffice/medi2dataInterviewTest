from rest_framework import serializers
from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

    def validate(self, data):
        start_time = data['start_time']
        end_time = data['end_time']

        # Check for appointments with overlapping time ranges
        existing_appointments = Appointment.objects.filter(
            start_time__lt=end_time,  # Existing appointment ends after the new one starts
            end_time__gt=start_time   # Existing appointment starts before the new one ends
        )

        # Exclude the current appointment
        if self.instance:
            existing_appointments = existing_appointments.exclude(id=self.instance.id)

        # If there are overlapping appointments, raise a validation error
        if existing_appointments.exists():
            raise serializers.ValidationError("Appointment time clashes with existing appointments.")

        return data
