from rest_framework import serializers

from api.questions.serializers import UserSerializer
from question.models import Comment, Question


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'count_like', 'created_at']
        read_only_fields = ['user', 'count_like', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
