from django import forms
from django.contrib.auth import get_user_model
from django.forms.widgets import Select
from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import PrefixChoiceField, SplitPhoneNumberField


class BootstrapSplitPhoneNumberField(SplitPhoneNumberField):
    def prefix_field(self):
        field = PrefixChoiceField(
            widget=Select(
                attrs={
                    "class": "form-select contry-code-select",
                    "autocomplete": "tel-country-code",
                    "style": "width: 40%;",
                }
            )
        )
        return field

    def number_field(self):
        return forms.CharField(
            widget=forms.TextInput(
                attrs={
                    "type": "tel",
                    "class": "form-control ms-2",
                    "autocomplete": "tel-national",
                    "area-describedby": "phoneNumberHelp",
                    "maxlength": 10,
                }
            )
        )


class UserForm(forms.ModelForm):
    phonenumber = BootstrapSplitPhoneNumberField(
        required=False,
        label=_("Номер телефона"),
    )

    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "phonenumber",
            "first_name",
            "last_name",
        )
        error_messages = {
            "email": {
                "unique": _("Пользователь с этой электронной почтой уже существует."),
                "required": _("Email нужно обязательно внести."),
            },
        }

    def clean_phonenumber(self):
        phonenumber = self.cleaned_data.get("phonenumber")
        if phonenumber:
            User = get_user_model()
            if not (pk := self.instance.pk):
                if User.objects.filter(phonenumber=phonenumber).exists():
                    raise forms.ValidationError(
                        _("Пользователь с этим номером телефона уже существует.")
                    )
            else:
                if User.objects.filter(phonenumber=phonenumber).exclude(pk=pk).exists():
                    raise forms.ValidationError(
                        _("Пользователь с этим номером телефона уже существует.")
                    )

        return phonenumber
