from rest_framework import status
from rest_framework.test import APITestCase
from ads.models import Ad
from users.models import User
from django.urls import reverse
from django.utils.timezone import localtime


class AdTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="user@example.com")
        self.not_author = User.objects.create(email="not_author@example.com")
        self.admin = User.objects.create(email="admin@example.com", role=User.ADMIN)
        self.ad = Ad.objects.create(title="Объявление", price=10000, description="Описание объявления", author=self.user)
        self.client.force_authenticate(user=self.user)

    def test_ad_create(self):
        url = reverse("ads:ad-list")
        data = {
            "title": "Тестовое название",
            "price": 5000,
            "description": "Тестовое описание"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ad.objects.all().count(), 2)

    def test_ad_retrieve(self):
        url = reverse("ads:ad-detail", args=(self.ad.pk,))
        response =self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.ad.title)

    def test_ad_list(self):
        url = reverse("ads:ad-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.ad.pk,
                    'title': self.ad.title,
                    'price': self.ad.price,
                    'description': self.ad.description,
                    'created_at': localtime(self.ad.created_at).isoformat(),
                    'author': self.ad.author.pk,
                 }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_ad_update(self):
        url = reverse("ads:ad-detail", args=(self.ad.pk,))
        data = {
            "title": "Тестовое название",
            "price": 5000,
            "description": "Тестовое описание"
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Тестовое название")

    def test_ad_delete(self):
        url = reverse("ads:ad-detail", args=(self.ad.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ad.objects.all().count(), 0)

    def test_ad_delete_without_permissions(self):
        self.client.force_authenticate(user=self.not_author)
        url = reverse("ads:ad-detail", args=(self.ad.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Ad.objects.filter(pk=self.ad.pk).exists())

    def test_ad_delete_by_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse("ads:ad-detail", args=(self.ad.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ad.objects.all().count(), 0)
