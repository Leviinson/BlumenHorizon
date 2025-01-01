from dataclasses import dataclass
from typing import NamedTuple, NewType, TypedDict

from django.urls import reverse_lazy

from accounts.models import User


@dataclass
class UrlsDataclass:
    signup: str = reverse_lazy("accounts:signup")
    signin: str = reverse_lazy("accounts:signin")
    profile: str = reverse_lazy("accounts:me")
    mainpage: str = reverse_lazy("mainpage:offers")


UserPassword = NewType("UserPassword", str)


class UserSignUpCredentials(TypedDict):
    email: str
    password1: str
    password2: str
    first_name: str
    last_name: str
    phonenumber_0: str
    phonenumber_1: str


class UserCredentials(TypedDict):
    email: str
    phonenumber: str
    first_name: str
    last_name: str


class UserData(NamedTuple):
    user: User
    password: UserPassword
