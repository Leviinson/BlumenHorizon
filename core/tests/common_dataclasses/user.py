from dataclasses import dataclass


@dataclass
class UserSignUpCredentials:
    email: str
    password1: str
    password2: str
    first_name: str
    last_name: str
    phonenumber_0: str = "DE"
    phonenumber_1: str = "15234815621"

@dataclass
class UserCredentials:
    email: str
    phonenumber: str
    first_name: str
    last_name: str
    password: str = None
