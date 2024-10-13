from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.views.generic.detail import DetailView


class UserDetailView(DetailView):
    model = get_user_model()
