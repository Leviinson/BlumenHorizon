from django.shortcuts import redirect
from django.urls import reverse_lazy


class NotAuthenticatedMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy("accounts:me"))
        return super().dispatch(request, *args, **kwargs)