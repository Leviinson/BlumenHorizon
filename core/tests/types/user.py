from typing import NewType, TypedDict

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
