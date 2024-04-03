from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from like.models import Like
from question.models import Question, Comment


class LikeToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        question_id = request.data.get('question_id')
        comment_id = request.data.get('comment_id')

        with transaction.atomic():
            if question_id:
                question = get_object_or_404(Question, id=question_id)
                like, created = Like.objects.get_or_create(user=user, question=question)
                if not created:
                    like.delete()
                    question.count_like -= 1
                else:
                    question.count_like += 1
                question.save()
                return Response({'liked': created, 'count_like': question.count_like},
                                status=status.HTTP_200_OK)
            elif comment_id:
                comment = get_object_or_404(Comment, id=comment_id)
                like, created = Like.objects.get_or_create(user=user, comment=comment)
                if not created:
                    like.delete()
                    comment.count_like -= 1
                else:
                    comment.count_like += 1
                comment.save()
                return Response({'liked': created, 'count_like': comment.count_like},
                                status=status.HTTP_200_OK)
        return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
