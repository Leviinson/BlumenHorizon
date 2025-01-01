from dataclasses import dataclass

from django.urls import reverse_lazy


@dataclass
class UrlsDataclass:
    signup: str = reverse_lazy("accounts:signup")
    signin: str = reverse_lazy("accounts:signin")
    profile: str = reverse_lazy("accounts:me")
    mainpage: str = reverse_lazy("mainpage:offers")
