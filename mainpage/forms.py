from django import forms
from django.utils.translation import gettext_lazy as _

from accounts.models import User
from core.forms import BootstrapSplitPhoneNumberField
from mainpage.models import IndividualOrder


class IndividualOrderForm(forms.ModelForm):
    phonenumber = BootstrapSplitPhoneNumberField(label=_("Номер телефона"))

    class Meta:
        model = IndividualOrder
        fields = ("first_name", "phonenumber")

    def save(self, commit=False, user: User = None):
        order: IndividualOrder = super().save(commit=False)
        if user.is_authenticated:
            order.user = user
        if commit:
            order.save()
        return order
