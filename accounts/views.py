from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404

from rest_framework.generics import (
    RetrieveAPIView,
)
from .serializers import UserAccountSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class SignupView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        data = self.request.data

        name = data["name"]
        email = data["email"]
        password = data["password"]
        password2 = data["password2"]

        if password == password2:
            if User.objects.filter(email=email).exists():
                return Response({"error": "Email already exists"})
            else:
                if len(password) < 6:
                    return Response({"error": "Password must be at least 6 characters"})
                else:
                    user = User.objects.create_user(
                        email=email, password=password, name=name
                    )

                    user.save()
                    return Response({"success": "User created successfully"})
        else:
            return Response({"error": "Passwords do not match"})


class BlacklistTokenView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(RetrieveAPIView):
    """Get user details by querying email field"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserAccountSerializer
    lookup_field = "email"
    queryset = User.objects.all()
