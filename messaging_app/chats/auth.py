from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication class (optional).
    You can extend this to add extra logic if needed.
    """
    def authenticate(self, request):
        user_auth_tuple = super().authenticate(request)
        if user_auth_tuple is None:
            return None
        user, token = user_auth_tuple
        # Add custom logic here if needed
        return (user, token)


def get_user_from_token(token):
    """
    Helper function to get a user from a JWT token string.
    """
    try:
        UntypedToken(token)
        validated_token = JWTAuthentication().get_validated_token(token)
        user = JWTAuthentication().get_user(validated_token)
        return user
    except (InvalidToken, TokenError):
        return None
