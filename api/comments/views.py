from django.db.models import Exists
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api.comments.filters import CommentCustomFilter
from api.comments.serializers import CommentSerializer
from like.models import Like
from question.models import Comment, Question

from django.db import transaction


class CommentUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        question = instance.question
        question.count_comment -= 1
        question.save()
        return super().perform_destroy(instance)


class CommentListView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = CommentCustomFilter

    def create(self, request, *args, **kwargs):
        question_id = request.query_params.get('question_id')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            serializer.save(question_id=question_id)
            question = Question.objects.get(id=question_id)
            question.count_comment += 1
            question.save()
        return Response(serializer.data, status=201)

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        from django.db.models import OuterRef
        queryset = queryset.annotate(liked=Exists(Like.objects.filter(user=user, comment=OuterRef('pk'))))
        return queryset
