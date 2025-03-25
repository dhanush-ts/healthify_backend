import jwt
from rest_framework import authentication, exceptions
from user_model.models import User
from django.utils import timezone
from datetime import datetime
from rest_framework.response import Response
from django.conf import settings

class IsAuthenticated(authentication.BaseAuthentication):
    def authenticate_header(self, request):
        return "Invalid token"

    def authenticate(self, request):
        try:
            token = request.headers.get('Authorization', '').split(' ')[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('id')
            user = User.objects.get(pk=user_id)
            if isinstance(user, User):
                return (user, token)
            return Response({"error": "No users found"}, status=404)
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token has expired")
        except jwt.exceptions.InvalidTokenError:
            raise exceptions.AuthenticationFailed("Invalid token")
        except IndexError:
            raise exceptions.AuthenticationFailed("No Token Provided")
        except Exception as e:
            print(e)
            raise exceptions.AuthenticationFailed("An error occurred while decoding token")

def generate_token(user):
    exp_date = datetime.now() + timezone.timedelta(days=365)
    return jwt.encode({
        'id': user.id,
        'exp': exp_date.timestamp()
    }, settings.SECRET_KEY, algorithm='HS256')