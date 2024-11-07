from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from core.forms import BootstrapSplitPhoneNumberField


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
