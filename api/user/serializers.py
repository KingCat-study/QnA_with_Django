from django.contrib.auth import authenticate
from rest_framework import serializers


class ObtainTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=150)
    password = serializers.CharField(required=True, max_length=128)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), username=username, password=password)

        if not user:
            msg = '아이디 또는 비밀번호가 일치하지 않습니다.'
            raise serializers.ValidationError(msg)

        attrs['user'] = user
        return attrs
