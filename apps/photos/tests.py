import io
import json

from django.contrib.auth.models import User
from django.core.files import File
from django.test import TestCase
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient

from .models import Photo

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse


class BaseTestCase(TestCase):
    def clearPhotos(self):
        Photo.objects.all().delete()

    def run(self, *args, **kwargs):

        self.clearPhotos()
        super(BaseTestCase, self).run(*args, **kwargs)
        self.clearPhotos()


class TestPhotoView(BaseTestCase):

    def setUp(self):
        self.api_client = APIClient()
        self.user1 = User.objects.create(username='user1')
        self.user1.set_password('user1')
        self.user1.save()
        self.user2 = User.objects.create(username='user2')

    def generate_photo_file(self, name='test.png'):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = name
        file.seek(0)
        return file

    def test_list_photos(self):
        url = reverse('photos-list')
        # Test without token access where the api cannot be called
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        token_url = reverse('token_obtain_pair')
        response = self.client.post(token_url,
                                    dict(username='user1', password='user1'), format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.json())
        access_token = response.json()['access']
        self.api_client.credentials(
            HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

        photo = Photo.objects.create(
            photo=self.generate_photo_file().name,
            caption='Test 1', user=self.user1
        )

        # Test get all photos
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 1)
        self.assertEqual(response.json()['results'][0]['caption'], 'Test 1')

        # Test get draft photos
        photo2 = Photo.objects.create(
            photo=self.generate_photo_file(name='test2.png').name,
            caption='Test 2', user=self.user2
        )
        response = self.api_client.get('{}?published=false'.format(url))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 2)

        # Test get published photos
        photo.publish()
        response = self.api_client.get('{}?published=true'.format(url))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 1)

        # Test ascending order by published date
        photo2.publish()
        response = self.api_client.get('{}?ordering=published_at'.format(url))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 2)
        self.assertEqual(response.json()['results'][0]['caption'], 'Test 1')
        self.assertEqual(response.json()['results'][1]['caption'], 'Test 2')

        # Test descending order by published date
        response = self.api_client.get('{}?ordering=-published_at'.format(url))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 2)
        self.assertEqual(response.json()['results'][0]['caption'], 'Test 2')
        self.assertEqual(response.json()['results'][1]['caption'], 'Test 1')

        # Test get photos by user
        response = self.api_client.get('{}?user={}'.format(url, self.user2.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['results']), 1)
        self.assertEqual(response.json()['results'][0]['caption'], 'Test 2')

    def test_create_photo(self):
        url = reverse('photos-list')
        # Test without token access where the api cannot be called
        response = self.api_client.post(url, {}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test with token access where we upload a photo
        token_url = reverse('token_obtain_pair')
        response = self.client.post(token_url,
                                    dict(username='user1', password='user1'), format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.json())
        access_token = response.json()['access']
        self.api_client.credentials(
            HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

        payload = dict(photo=self.generate_photo_file(),
                       caption='Test 1', user=self.user1.id)

        response = self.api_client.post(
            url,
            payload,
            format='multipart')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['caption'], 'Test 1')

    def test_publish_photo(self):
        photo = Photo.objects.create(
            photo=self.generate_photo_file().name,
            caption='Test 1', user=self.user1
        )
        url = reverse('photos-publish', kwargs={'pk': photo.pk})
        # Test without token access where the api cannot be called
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test with token access where we publish a photo
        token_url = reverse('token_obtain_pair')
        response = self.client.post(token_url,
                                    dict(username='user1', password='user1'), format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.json())
        access_token = response.json()['access']

        self.api_client.credentials(
            HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

        self.assertIsNone(photo.published_at)

        response = self.api_client.post(url, {}, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json()['published_at'])

    def test_get_photo(self):
        photo = Photo.objects.create(
            photo=self.generate_photo_file().name,
            caption='Test 1', user=self.user1
        )
        url = reverse('photos-detail', kwargs={'pk': photo.pk})
        # Test without token access where the api cannot be called
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test with token access where we get photo details
        token_url = reverse('token_obtain_pair')
        response = self.client.post(token_url,
                                    dict(username='user1', password='user1'), format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.json())
        access_token = response.json()['access']

        self.api_client.credentials(
            HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

        response = self.api_client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['caption'], 'Test 1')

    def test_edit_photo(self):
        photo = Photo.objects.create(
            photo=self.generate_photo_file().name,
            caption='Test 1', user=self.user1
        )
        url = reverse('photos-detail', kwargs={'pk': photo.pk})
        # Test without token access where the api cannot be called
        response = self.api_client.put(url, {}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test with token access where the photo can be updated
        token_url = reverse('token_obtain_pair')
        response = self.client.post(token_url,
                                    dict(username='user1', password='user1'), format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.json())
        access_token = response.json()['access']

        self.api_client.credentials(
            HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

        payload = dict(photo=self.generate_photo_file(),
                       caption='Test 2', user=self.user1.id)
        response = self.api_client.put(url, payload, format='multipart')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['caption'], 'Test 2')

    def test_delete_photo(self):
        photo = Photo.objects.create(
            photo=self.generate_photo_file().name,
            caption='Test 1', user=self.user1
        )
        url = reverse('photos-detail', kwargs={'pk': photo.pk})
        # Test without token access where the api cannot be called
        response = self.api_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test with token access where the photo can be deleted
        token_url = reverse('token_obtain_pair')
        response = self.client.post(token_url,
                                    dict(username='user1', password='user1'), format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.json())
        access_token = response.json()['access']
        self.api_client.credentials(
            HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

        response = self.api_client.delete(url)

        self.assertEqual(response.status_code, 204)

    def test_batch_edit_photo(self):
        url = reverse('batch_edit')
        # Test without token access where the api cannot be called
        response = self.api_client.put(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test with token access where photo captions can be edited
        token_url = reverse('token_obtain_pair')
        response = self.client.post(token_url,
                                    dict(username='user1', password='user1'), format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.json())
        access_token = response.json()['access']

        self.api_client.credentials(
            HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

        photo = Photo.objects.create(
            photo=self.generate_photo_file().name,
            caption='Test 1', user=self.user1
        )
        payload = [dict(id=photo.id, caption='Test Update')]
        response = self.api_client.put(url, payload, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['caption'], 'Test Update')

    def test_batch_publish_photo(self):
        url = reverse('batch_publish')
        # Test without token access where the api cannot be called
        response = self.api_client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test with token access where photos can be publish in batch
        token_url = reverse('token_obtain_pair')
        response = self.client.post(token_url,
                                    dict(username='user1', password='user1'), format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.json())
        access_token = response.json()['access']

        self.api_client.credentials(
            HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

        photo = Photo.objects.create(
            photo=self.generate_photo_file().name,
            caption='Test 1', user=self.user1
        )
        self.assertIsNone(photo.published_at)
        payload = dict(ids=[photo.id])
        response = self.api_client.post(url, payload, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json()[0]['published_at'])

    def test_batch_delete_photo(self):
        url = reverse('batch_delete')
        # Test without token access where the api cannot be called
        response = self.api_client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test with token access where photos can be deleted in batch
        token_url = reverse('token_obtain_pair')
        response = self.client.post(token_url,
                                    dict(username='user1', password='user1'), format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.json())
        access_token = response.json()['access']

        self.api_client.credentials(
            HTTP_AUTHORIZATION='Bearer {}'.format(access_token))

        photo = Photo.objects.create(
            photo=self.generate_photo_file().name,
            caption='Test 1', user=self.user1
        )
        payload = dict(ids=[photo.id])
        response = self.api_client.post(url, payload, format='json')

        self.assertEqual(response.status_code, 204)
