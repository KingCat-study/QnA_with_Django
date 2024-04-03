from api.questions.serializers import QuestionSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from like.models import Like
from question.models import Question

from rest_framework.response import Response


# api를 function based view 로 만들건데 Question 모델로 database 에 전체 조회고 이를 시리얼 라이즈 해서 응답으로 내보내는 api 를 만들거야
# @api_view(['GET'])
# def question_list_view(request):
#     queryset = Question.objects.all()
#     serializer = QuestionSerializer(queryset, many=True)
#     return Response(serializer.data)

# () tuple
# [] list
# {} dict
class QuestionListView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ['title__contains']
    filterset_fields = ['user_id']
    ordering_fields = ['created_at', 'count_like']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]


class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        user = request.user
        liked_question = False

        if user.is_authenticated:
            liked_question = Like.objects.filter(question_id=instance.id, user_id=user.id).exists()

        serializer = self.get_serializer(instance)
        data = serializer.data
        data['liked_question'] = liked_question

        return Response(data)