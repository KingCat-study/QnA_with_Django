from django.contrib.auth import get_user_model
from rest_framework import serializers

from question.models import Question

User = get_user_model()  # 유저  모델 가져오기


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        read_only_fields = ['id', 'username']


class QuestionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'title', 'content', 'count_like', 'count_comment', 'user', 'created_at', 'modified_at']
        read_only_fields = ['count_like', 'count_comment']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


