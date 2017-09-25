from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegistrationSerializer, LoginSerializer, UserSerializer, UserUpdateSerializer
from rest_framework.exceptions import NotFound, ValidationError

from .renderers import UserJSONRenderer
from .models import User

class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data,  status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer
    update_serializer_class = UserUpdateSerializer

    queryset = User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        serializer_context = {'request': request}
        username = request.query_params.get('username', None)
        phonenum = request.query_params.get('phonenum', None)
        if username is not None:
            try:
                self.queryset = self.queryset.get(name=username)
            except User.DoesNotExist:
                raise NotFound('An user with this username does not exists.')
        elif phonenum is not None:
            try:
                self.queryset = self.queryset.get(phonenum=phonenum)
            except User.DoesNotExist:
                raise NotFound('An user with this phonenum does not exists.')
        else:
            self.queryset = self.queryset.get(id=request.user.id)
        try:
            serializer_instance = self.queryset
        except User.DoesNotExist:
            raise NotFound('An user with this phonenum/name does not exists.')

        serializer = self.serializer_class(serializer_instance,
                                           context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):

        serializer_data = request.data.get('user', {})
        updating_user_name = serializer_data.get('name', None)

        if updating_user_name != request.user.name :
            return Response({'error': 'cannot update other user'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.update_serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)