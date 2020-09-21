from django.contrib.auth import get_user_model
from rest_framework import response, decorators, permissions, status, exceptions
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserCreateSerializer

User = get_user_model()


@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def registration(request):
    serializer = UserCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return response.Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    user = serializer.save()
    refresh = RefreshToken.for_user(user)
    res = {
        'user_id': user.id,
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
    return response.Response(res, status.HTTP_201_CREATED)


@decorators.api_view(["POST"])
@decorators.permission_classes([permissions.AllowAny])
def login(request):
    User = get_user_model()
    email = request.data.get('email')
    password = request.data.get('password')

    if (email is None) or (password is None):
        raise exceptions.AuthenticationFailed('username and password required')

    user = User.objects.filter(email=email).first()
    if user is None:
        raise exceptions.AuthenticationFailed('user not found')
    if not user.check_password(password):
        raise exceptions.AuthenticationFailed('wrong password')

    refresh = RefreshToken.for_user(user)
    res = {
        'user_id': user.id,
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
    return response.Response(res, status.HTTP_202_ACCEPTED)
