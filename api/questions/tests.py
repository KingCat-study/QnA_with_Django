from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from question.models import Question

User = get_user_model()


class QuestionTest(APITestCase):

    # 전체 테스트 케이스에서 사용할 데이터 설정
    # @classmethod
    # def setUpTestData(cls):
    #     pass

    # 테스트 케이스가 실행될 때 마다 전처리할 데이터 설정
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='root1234')
        self.token = Token.objects.create(user=self.user)
        self.question = Question.objects.create(user=self.user, title='test1', content='test1')

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_question_list(self):
        url = reverse('question_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['title'], 'test1')

    def test_question_create(self):
        self.authenticate()
        data = {
            'title': 'New Question',
            'content': 'Content of the new question'
        }
        url = reverse('question_list')
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], 'New Question')
        self.assertEqual(response.data['content'], 'Content of the new question')
        self.assertEqual(response.data['user'], {'id': 1, 'username': 'testuser'})

    def test_question_detail(self):
        url = reverse('question_detail', kwargs={'pk': self.question.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'test1')
        self.assertEqual(response.data['content'], 'test1')
        self.assertEqual(response.data['user'], {'id': 1, 'username': 'testuser'})

    def test_question_update(self):
        self.authenticate()
        data = {
            'title': 'Updated Question',
            'content': 'Content of the updated question'
        }
        url = reverse('question_detail', kwargs={'pk': self.question.id})
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Updated Question')
        self.assertEqual(response.data['content'], 'Content of the updated question')
        self.assertEqual(response.data['user'], {'id': 1, 'username': 'testuser'})

    def test_question_delete(self):
        url = reverse('question_detail', kwargs={'pk': self.question.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Question.objects.count(), 0)
        self.assertEqual(response.data, None)
        self.assertEqual(response.content, b'')
        self.assertEqual(Question.objects.filter(pk=self.question.id).exists(), False)
