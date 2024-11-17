import logging
from .serializers import UserSerializer, LoginSerializer
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

# Get an instance of a logger
logger = logging.getLogger(__name__)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            # Authenticate the user
            user = authenticate(username=username, password=password)
            if user is not None:
                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }, status=status.HTTP_200_OK)
            else:
                logger.error(f"Failed login attempt for username: {username}")
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        logger.error(f"Login failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "username": user.username,
            }, status=status.HTTP_201_CREATED)

        logger.error(f"Registration failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # Look for the refresh token in the request body
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            logger.error("No refresh token provided in the request body")
            return Response({"error": "No refresh token provided"}, status=status.HTTP_400_BAD_REQUEST)

        logger.info(f"Received refresh token: {refresh_token}")

        try:
            # Decode the refresh token to get the user data
            refresh = RefreshToken(refresh_token)
            # Generate a new access token using the refresh token
            new_access_token = str(refresh.access_token)
            logger.info(f"New access token generated: {new_access_token}")
            return Response({"access": new_access_token}, status=status.HTTP_200_OK)

        except AuthenticationFailed as e:
            logger.error(f"Invalid or expired refresh token: {str(e)}")
            return Response({"error": "Invalid or expired refresh token"}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            logger.error(f"Failed to refresh access token: {str(e)}")
            return Response({"error": "Failed to refresh access token"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)