from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework import status
from .models import Patient, MedicalRecord
from users.models import User


class PatientTestCase(TestCase):
    def setUp(self):
        # test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Authenticate client
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_create_patient(self):
        data = {
            'name': 'Paul Pogba',
            'date_of_birth': '1990-01-01',
            'gender': 'M',
            'contact_information': 'paul@example.com'
        }
        response = self.client.post('/patient/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patient.objects.count(), 1)

    def test_retrieve_patient(self):
        patient = Patient.objects.create(
            name='Paul Pogba',
            date_of_birth='1990-01-01',
            gender='M',
            contact_information='paul@example.com'
        )
        response = self.client.get(f'/patient/{patient.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Paul Pogba')

    def test_update_patient(self):
        patient = Patient.objects.create(
            name='Paul Pogba',
            date_of_birth='1990-01-01',
            gender='M',
            contact_information='paul@example.com'
        )
        data = {
            'name': 'Updated Name',
            'date_of_birth': '1995-02-02',
            'gender': 'F',
            'contact_information': 'updated@example.com'
        }
        response = self.client.put(f'/patient/{patient.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Patient.objects.get(id=patient.id).name, 'Updated Name')

    def test_delete_patient(self):
        patient = Patient.objects.create(
            name='Paul Pogba',
            date_of_birth='1990-01-01',
            gender='M',
            contact_information='paul@example.com'
        )
        response = self.client.delete(f'/patient/{patient.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Patient.objects.count(), 0)

    def test_list_patients(self):
        Patient.objects.create(
            name='Patient 1',
            date_of_birth='1990-01-01',
            gender='M',
            contact_information='patient1@example.com'
        )
        Patient.objects.create(
            name='Patient 2',
            date_of_birth='1995-02-02',
            gender='F',
            contact_information='patient2@example.com'
        )
        response = self.client.get('/patient/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_delete_nonexistent_patient(self):
        response = self.client.delete('/patient/1001/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_nonexistent_patient(self):
        data = {
            'name': 'Updated Name',
            'date_of_birth': '1995-02-02',
            'gender': 'F',
            'contact_information': 'updated@example.com'
        }
        response = self.client.put('/patients/1001/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_patient_invalid_data(self):
        data = {
            'name': 'Paul Pogba',
            'date_of_birth': 'invalid_date_format',  # Invalid date format
            'gender': 'M',
            'contact_information': 'paul@example.com'
        }
        response = self.client.post('/patient/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_patient_invalid_data(self):
        patient = Patient.objects.create(
            name='Paul Pogba',
            date_of_birth='1990-01-01',
            gender='M',
            contact_information='paul@example.com'
        )
        data = {
            'name': '',  # Name cannot be empty
            'date_of_birth': '1995-02-02',
            'gender': 'F',
            'contact_information': 'updated@example.com'
        }
        response = self.client.put(f'/patient/{patient.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class MedicalRecordTestCase(TestCase):
    """
        Test cases for the Medical Records
    """

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a patient
        self.patient = Patient.objects.create(
            name='Paul Pogba',
            date_of_birth='1990-01-01',
            gender='M',
            contact_information='paul@example.com'
        )

        # Create an authentication token for the test user
        self.token = Token.objects.create(user=self.user)

        # Authenticate the client using the token
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_create_medical_record(self):
        data = {
            'patient': self.patient.id,
            'allergies': 'Pollen',
            'medications': 'Aspirin',
            'previous_illnesses': 'Flu',
            'surgeries': 'Appendectomy'
        }
        response = self.client.post(f'/patient/{self.patient.id}/medical-records/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MedicalRecord.objects.count(), 1)

    def test_retrieve_medical_record(self):
        medical_record = MedicalRecord.objects.create(
            patient=self.patient,
            allergies='Pollen',
            medications='Aspirin',
            previous_illnesses='Flu',
            surgeries='Appendectomy'
        )
        response = self.client.get(f'/patient/medical-record/{medical_record.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['allergies'], 'Pollen')

    def test_update_medical_record(self):
        medical_record = MedicalRecord.objects.create(
            patient=self.patient,
            allergies='Pollen',
            medications='Aspirin',
            previous_illnesses='Flu',
            surgeries='Appendectomy'
        )
        data = {
            'allergies': 'Updated Allergies',
            'medications': 'Updated Medications',
            'previous_illnesses': 'Updated Illnesses',
            'surgeries': 'Updated Surgeries'
        }
        response = self.client.put(f'/patient/medical-record/{medical_record.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(MedicalRecord.objects.get(id=medical_record.id).allergies, 'Updated Allergies')

    def test_delete_medical_record(self):
        medical_record = MedicalRecord.objects.create(
            patient=self.patient,
            allergies='Pollen',
            medications='Aspirin',
            previous_illnesses='Flu',
            surgeries='Appendectomy'
        )
        response = self.client.delete(f'/patient/medical-record/{medical_record.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MedicalRecord.objects.count(), 0)

    def test_list_medical_records(self):
        MedicalRecord.objects.create(
            patient=self.patient,
            allergies='Pollen',
            medications='Aspirin',
            previous_illnesses='Flu',
            surgeries='Appendectomy'
        )
        MedicalRecord.objects.create(
            patient=self.patient,
            allergies='Dust',
            medications='Ibuprofen',
            previous_illnesses='Cough',
            surgeries='Tonsillectomy'
        )
        response = self.client.get(f'/patient/{self.patient.id}/medical-records/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_delete_nonexistent_medical_record(self):
        response = self.client.delete('/patient/medical-record/1001/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_nonexistent_medical_record(self):
        data = {
            'allergies': 'Updated Allergies',
            'medications': 'Updated Medications',
            'previous_illnesses': 'Updated Illnesses',
            'surgeries': 'Updated Surgeries'
        }
        response = self.client.put('/patient/medical-record/1001/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_medical_record_invalid_data(self):
        data = {
            'patient': "",  # Here patient_id is not supplied
            'medications': 'Aspirin',
            'previous_illnesses': 'Flu',
            'surgeries': 'Appendectomy'
        }
        response = self.client.post(f'/patient/{self.patient.id}/medical-records/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_medical_record_invalid_data(self):
        medical_record = MedicalRecord.objects.create(
            patient=self.patient,
            allergies='Pollen',
            medications='Aspirin',
            previous_illnesses='Flu',
            surgeries='Appendectomy'
        )
        data = {
            'allergies': False,  # Allergies cannot be a Boolean
            'medications': 'Updated Medications',
            'previous_illnesses': 'Updated Illnesses',
            'surgeries': 'Updated Surgeries'
        }
        response = self.client.put(f'/patient/medical-record/{medical_record.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
