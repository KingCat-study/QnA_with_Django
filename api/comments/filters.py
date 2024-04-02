from django_filters import rest_framework as filters
from rest_framework.exceptions import ValidationError

from question.models import Comment, Question


class CommentCustomFilter(filters.FilterSet):
    question_id = filters.NumberFilter(method="question_id_filter", required=True)

    class Meta:
        model = Comment
        fields = ['question_id']

    def question_id_filter(self, queryset, name, value):
        if not Question.objects.filter(id=value).exists():
            raise ValidationError("Question does not exist.")
        return queryset.filter(**{name : value})
