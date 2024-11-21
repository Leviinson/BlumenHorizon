from django import forms
from django.forms.widgets import Select
from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import SplitPhoneNumberField

from .fields import CountryCodePrefixChoiceField


class BootstrapSplitPhoneNumberField(SplitPhoneNumberField):
    def prefix_field(self):
        field = CountryCodePrefixChoiceField(
            widget=Select(
                attrs={
                    "class": "form-select contry-code-select text-start",
                    "autocomplete": "tel-country-code",
                    "style": "width: 60%;",
                }
            )
        )
        return field

    def number_field(self):
        return forms.CharField(
            widget=forms.TextInput(
                attrs={
                    "type": "tel",
                    "class": "form-control ms-2 text-start",
                    "autocomplete": "tel-national",
                    "area-describedby": "phoneNumberHelp",
                    "maxlength": 12,
                }
            )
        )
