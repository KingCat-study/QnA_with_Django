from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.user.serializers import ObtainTokenSerializer


class ObtainTokenView(APIView):
    serializer_class = ObtainTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, is_create = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

    def delete(self, request, *args, **kwargs):
        Token.objects.get(user=request.user).delete()
        return Response(status=204)

    def get_permissions(self):
        if self.request.method == 'POST':
            return []
        elif self.request.method == 'DELETE':
            return [IsAuthenticated()]
        return super().get_permissions()



