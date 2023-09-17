from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from .models import Appointment
from datetime import datetime, timedelta
from patients.models import Patient
from users.models import User


class AppointmentTestCase(TestCase):
    def setUp(self):
        # test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # patient instance
        self.patient = Patient.objects.create(
            name='Paul Pogba',
            date_of_birth='1990-01-01',
            gender='M',
            contact_information='paul@example.com'
        )

        # appointment instance
        self.appointment = Appointment.objects.create(
            patient=self.patient,
            start_time=timezone.now() + timedelta(days=1, hours=2),
            end_time=timezone.now() + timedelta(days=1, hours=3),
            description='Test appointment'
        )

        # Authenticate client
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_create_appointment(self):
        data = {
            'patient': self.patient.id,
            'start_time': (timezone.now() + timedelta(days=2)).isoformat(),
            'end_time': (timezone.now() + timedelta(days=2, hours=1)).isoformat(),
            'description': 'New appointment'
        }
        response = self.client.post('/appointment/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 2)

    def test_retrieve_appointment(self):
        response = self.client.get(f'/appointment/{self.appointment.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], 'Test appointment')

    def test_update_appointment(self):
        data = {
            'patient': self.patient.id,
            'start_time': (timezone.now() + timedelta(days=1, hours=4)).isoformat(),
            'end_time': (timezone.now() + timedelta(days=1, hours=5)).isoformat(),
            'description': 'Updated appointment'
        }
        response = self.client.put(f'/appointment/{self.appointment.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Appointment.objects.get(id=self.appointment.id).description, 'Updated appointment')

    def test_delete_appointment(self):
        response = self.client.delete(f'/appointment/{self.appointment.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Appointment.objects.count(), 0)

    def test_appointment_clash(self):
        data = {
            'patient': self.patient.id,
            'start_time': (timezone.now() + timedelta(days=1, hours=2)).isoformat(),
            'end_time': (timezone.now() + timedelta(days=1, hours=4)).isoformat(),
            'description': 'Clashing appointment'
        }
        response = self.client.post('/appointment/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthenticated_access(self):
        self.client.logout()
        response = self.client.get('/appointment/list/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_appointments(self):
        response = self.client.get('/appointment/list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_delete_nonexistent_appointment(self):
        response = self.client.delete('/appointment/1001/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_nonexistent_appointment(self):
        data = {
            'start_time': (timezone.now() + timedelta(days=1, hours=4)).isoformat(),
            'end_time': (timezone.now() + timedelta(days=1, hours=5)).isoformat(),
            'description': 'Updated appointment'
        }
        response = self.client.put('/appointment/1001/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_appointment_invalid_data(self):
        data = {
            'start_time': (timezone.now() + timedelta(days=1, hours=4)).isoformat(),
            'end_time': (timezone.now() + timedelta(days=1, hours=-1)).isoformat(),  # End time before start time
            'description': 'Invalid appointment'
        }
        response = self.client.post('/appointment/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_appointment_invalid_data(self):
        data = {
            'start_time': (datetime.now() + timedelta(days=1, hours=2)).isoformat(),
            'end_time': (datetime.now() + timedelta(days=1, hours=-1)).isoformat(),  # End time before start time
            'description': 'Invalid appointment'
        }
        response = self.client.put(f'/appointment/{self.appointment.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
