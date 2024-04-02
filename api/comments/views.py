from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api.comments.filters import CommentCustomFilter
from api.comments.serializers import CommentSerializer
from question.models import Comment, Question


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

        try:
            serializer.save(question_id=question_id)
        except Exception as e:
            raise ValidationError({"error": str(e)})
        else:
            question = Question.objects.get(id=question_id)
            question.count_comment += 1
            question.save()
        return Response(serializer.data, status=201)
