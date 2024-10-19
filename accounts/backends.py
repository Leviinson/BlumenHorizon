from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class UserAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return

        user_query = UserModel.objects.filter(
            Q(email=username) | Q(phonenumber=username)
        ).all()

        if user_query.exists() and len(user_query) < 2:
            user = user_query.first()
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None
