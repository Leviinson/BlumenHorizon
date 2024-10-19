from pprint import pprint

from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from .user_form import UserForm


class UserSignUpForm(UserCreationForm, UserForm):
    class Meta(UserForm.Meta):
        pass

    def clean_username(self):
        raise NotImplementedError(
            "Field 'username' is not supported by this version of User model."
        )
