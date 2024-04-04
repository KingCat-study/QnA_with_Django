from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
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

        error_response = self.validate_error(question_id, comment_id)
        if error_response:
            return error_response

        object_id = question_id or comment_id
        model = Question if question_id else Comment

        with transaction.atomic():
            response_data = self.toggle_like(user, object_id, model)

        return Response(response_data, status=status.HTTP_200_OK)

    def toggle_like(self, user, object_id, model):
        toggle_object = get_object_or_404(model, id=object_id)
        like, created = Like.objects.get_or_create(user=user, **{model.__name__.lower(): toggle_object})

        if not created:
            like.delete()
            toggle_object.count_like -= 1
        else:
            toggle_object.count_like += 1

        toggle_object.save()

        return {'liked': created, 'count_like': toggle_object.count_like}

    def validate_error(self, question_id, comment_id):
        if question_id and comment_id:
            return Response({'error': 'Both question_id and comment_id provided'},
                            status=status.HTTP_400_BAD_REQUEST)
            # question_id와 comment_id 둘 다 존재하지 않는 경우
        if not question_id and not comment_id:
            return Response({'error': 'Neither question_id nor comment_id provided'},
                            status=status.HTTP_400_BAD_REQUEST)
        return None
