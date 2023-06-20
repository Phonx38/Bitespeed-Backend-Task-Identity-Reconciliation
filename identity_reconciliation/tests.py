from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Contact


class ContactTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.primary_contact = Contact.objects.create(
            id=1, email="lorraine@hillvalley.edu", phoneNumber="123456"
        )
        self.secondary_contact = Contact.objects.create(
            id=23,
            email="mcfly@hillvalley.edu",
            phoneNumber="123456",
            linkedId=1,
            linkPrecedence="secondary",
        )

    def test_identify_existing_primary_contact(self):
        response = self.client.post(
            reverse("identify"),
            {"email": "lorraine@hillvalley.edu", "phoneNumber": "123456"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["contact"]["primaryContactId"], 1)
        self.assertListEqual(
            response.data["contact"]["emails"],
            ["lorraine@hillvalley.edu", "mcfly@hillvalley.edu"],
        )
        self.assertListEqual(response.data["contact"]["phoneNumbers"], ["123456"])
        self.assertListEqual(response.data["contact"]["secondaryContactIds"], [23])

    def test_identify_existing_secondary_contact(self):
        response = self.client.post(
            reverse("identify"),
            {"email": "mcfly@hillvalley.edu", "phoneNumber": "123456"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["contact"]["primaryContactId"], 1)
        self.assertListEqual(
            response.data["contact"]["emails"],
            ["lorraine@hillvalley.edu", "mcfly@hillvalley.edu"],
        )
        self.assertListEqual(response.data["contact"]["phoneNumbers"], ["123456"])
        self.assertListEqual(response.data["contact"]["secondaryContactIds"], [23])

    def test_identify_non_existing_contact(self):
        response = self.client.post(
            reverse("identify"),
            {"email": "unknown@unknown.com", "phoneNumber": "99999999"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["contact"]["emails"], ["unknown@unknown.com"])
        self.assertEqual(response.data["contact"]["phoneNumbers"], ["99999999"])
        self.assertListEqual(response.data["contact"]["secondaryContactIds"], [])

    def test_identify_no_email(self):
        response = self.client.post(
            reverse("identify"), {"phoneNumber": "123456"}, format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["contact"]["primaryContactId"], 1)
        self.assertListEqual(
            response.data["contact"]["emails"],
            ["lorraine@hillvalley.edu", "mcfly@hillvalley.edu"],
        )
        self.assertListEqual(response.data["contact"]["phoneNumbers"], ["123456"])
        self.assertListEqual(response.data["contact"]["secondaryContactIds"], [23])

    def tearDown(self):
        Contact.objects.all().delete()
