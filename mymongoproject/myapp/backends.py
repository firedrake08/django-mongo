from django.contrib.auth.backends import BaseBackend
from .models import User
from mongoengine.errors import DoesNotExist


class MongoEngineBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
            return None
        except DoesNotExist:
            return None
        except Exception:
            return None  # Handle other potential exceptions

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except DoesNotExist:
            return None
        except Exception:
            return None  # Handle other potential exceptions