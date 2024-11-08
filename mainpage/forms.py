from django import forms
from django.utils.translation import gettext_lazy as _

from accounts.models import User
from mainpage.models import IndividualOrder


class IndividualOrderForm(forms.ModelForm):

    class Meta:
        model = IndividualOrder
        fields = ("first_name", "contact_method", "recall_me")
        widgets = {
            "contact_method": forms.Textarea(
                attrs={
                    "style": "height: 60px; width: 100%",
                    "resize": "vertical",
                    "class": "form-control",
                    "id": "contact-method-input",
                    "autocomplete": "tel",
                }
            ),
        }

    def save(self, commit=False, user: User = None):
        order: IndividualOrder = super().save(commit=False)
        if user and user.is_authenticated:
            order.user = user
        order.save(commit)
        return order
