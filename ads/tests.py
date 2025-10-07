from rest_framework import status
from rest_framework.test import APITestCase
from ads.models import Ad, Review
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

    def test_ad_list_pagination(self):
        for i in range(5):
            Ad.objects.create(
                title=f"Объявление {i}",
                price=1000 + i,
                description="Описание",
                author=self.user
            )
        url = reverse("ads:ad-list")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLessEqual(len(data['results']), 4)
        self.assertIn('next', data)
        self.assertIn('previous', data)

    def test_ad_list_search(self):
        Ad.objects.create(title="Кофеварка", price=2000, description="Описание", author=self.user)
        Ad.objects.create(title="Телевизор", price=3000, description="Описание", author=self.user)
        Ad.objects.create(title="Холодильник", price=4000, description="Описание", author=self.user)

        url = reverse("ads:ad-list") + "?search=Кофеварка"
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['results'][0]['title'], "Кофеварка")

class ReviewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="user@example.com")
        self.not_author = User.objects.create(email="not_author@example.com")
        self.admin = User.objects.create(email="admin@example.com", role=User.ADMIN)
        self.ad = Ad.objects.create(title="Тестовое объявление", price=10000, description="Тестовое описание", author=self.not_author)
        self.review = Review.objects.create(text="Тестовый отзыв", author=self.user, ad=self.ad)
        self.client.force_authenticate(user=self.user)

    def test_review_create(self):
        url = reverse("ads:ad-reviews-list", args=(self.ad.pk,))
        data = {
            "text": "Отзыв",
            "ad": self.ad.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.all().count(), 2)

    def test_review_list(self):
        url = reverse("ads:ad-reviews-list", args=(self.ad.pk,))
        response = self.client.get(url)
        data = response.json()
        result = [
            {
                "id": self.review.pk,
                "text": self.review.text,
                "created_at": localtime(self.review.created_at).isoformat(),
                "author": self.user.pk,
                "ad": self.ad.pk
            }
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_review_retrieve(self):
        url = reverse("ads:ad-reviews-detail", kwargs={"ad_pk": self.ad.pk, "pk": self.review.pk})
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("text"), self.review.text)

    def test_review_update(self):
        url = reverse("ads:ad-reviews-detail", kwargs={"ad_pk": self.ad.pk, "pk": self.review.pk})
        data = {
            "text": "Тестовый отзыв обновленный"
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("text"), "Тестовый отзыв обновленный")

    def test_review_delete(self):
        url = reverse("ads:ad-reviews-detail", kwargs={"ad_pk": self.ad.pk, "pk": self.review.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Review.objects.all().count(), 0)

    def test_review_delete_without_permissions(self):
        self.client.force_authenticate(user=self.not_author)
        url = reverse("ads:ad-reviews-detail", kwargs={"ad_pk": self.ad.pk, "pk": self.review.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Review.objects.filter(pk=self.review.pk).exists())
        self.assertTrue(Ad.objects.filter(pk=self.ad.pk).exists())

    def test_review_delete_by_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse("ads:ad-reviews-detail", kwargs={"ad_pk": self.ad.pk, "pk": self.review.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Review.objects.all().count(), 0)
