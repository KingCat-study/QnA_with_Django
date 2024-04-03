from rest_framework import serializers

from api.questions.serializers import UserSerializer
from question.models import Comment, Question


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    liked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'count_like', 'created_at', 'liked']
        read_only_fields = ['user', 'count_like', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)

    def get_liked(self, obj):
        request = self.context.get('request')
        user = request.user if request else None
        if user and user.is_authenticated:
            liked_comments = user.like_set.filter(comment=obj)
            return liked_comments.exists()
        return False
