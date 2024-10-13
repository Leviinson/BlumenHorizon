from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password


class UserAuthenticationBackend(BaseBackend):
    def authenticate(
        self, request, username=None, password=None, phone_number=None, **kwargs
    ):
        User = get_user_model()
        try:
            match username, phone_number:
                case _, None:
                    user = User.objects.get(username=username)
                case None, _:
                    user = User.objects.get(phone_number=phone_number)
                case _:
                    return None

            if check_password(password, user.password):
                return user
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            return None
        return super().authenticate(request, username, password, phone_number, **kwargs)
