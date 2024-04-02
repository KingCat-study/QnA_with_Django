from urllib.parse import urlencode
from django.urls import reverse
from rest_framework.test import APITestCase

from question.models import Question, Comment
from user.models import User


class CommentsTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpassword')
        self.question = Question.objects.create(title='Test Question', content='Test content', user=self.user)
        self.comment_data = {'content': 'Test comment', 'question': self.question.id}
        self.create_url = reverse('comment_list')

    def test_comment_create(self):
        self.client.force_authenticate(user=self.user)
        url = f"{self.create_url}?{urlencode({'question_id': self.question.id})}"
        response = self.client.post(url, self.comment_data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().content, 'Test comment')

    def test_comment_list(self):
        url = f"{self.create_url}?{urlencode({'question_id': self.question.id})}"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 0)

    def test_comment_update(self):
        self.client.force_authenticate(user=self.user)
        comment = Comment.objects.create(content='Test comment', question=self.question, user=self.user)
        url = reverse('comment_update_delete', args=[comment.id])
        response = self.client.put(url, {'content': 'Updated comment'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.get().content, 'Updated comment')

    def test_comment_delete(self):
        self.client.force_authenticate(user=self.user)
        url = f"{self.create_url}?{urlencode({'question_id': self.question.id})}"
        response = self.client.post(url, self.comment_data)

        self.question.count_comment += 1
        self.question.save()
        self.assertEqual(self.question.count_comment, 1)

        url = reverse('comment_update_delete', args=[response.data.pop('id')])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.question.count_comment, 1)
