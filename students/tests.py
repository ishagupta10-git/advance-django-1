from rest_framework import status
from rest_framework.test import APITestCase

from .models import Student


class StudentAPITests(APITestCase):
    def setUp(self):
        self.student = Student.objects.create(
            name='Asha', email='asha@example.com', age=20, course='CS')
        self.payload = {'name': 'Ravi', 'email': 'ravi@example.com', 'age': 21, 'course': 'Math'}

    def test_list(self):
        r = self.client.get('/api/students/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 1)

    def test_create(self):
        r = self.client.post('/api/students/', self.payload, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 2)

    def test_create_invalid(self):
        r = self.client.post('/api/students/', {'name': 'x'}, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve(self):
        r = self.client.get(f'/api/students/{self.student.pk}/')
        self.assertEqual(r.data['email'], 'asha@example.com')

    def test_retrieve_missing(self):
        self.assertEqual(self.client.get('/api/students/999/').status_code, 404)

    def test_put(self):
        r = self.client.put(f'/api/students/{self.student.pk}/', self.payload, format='json')
        self.assertEqual(r.data['name'], 'Ravi')

    def test_patch(self):
        r = self.client.patch(f'/api/students/{self.student.pk}/', {'age': 30}, format='json')
        self.assertEqual(r.data['age'], 30)

    def test_delete(self):
        r = self.client.delete(f'/api/students/{self.student.pk}/')
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Student.objects.count(), 0)
