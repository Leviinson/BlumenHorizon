from typing import Optional

from django import forms

from accounts.models import User
from mainpage.models import IndividualOrder


class IndividualOrderForm(forms.ModelForm):

    class Meta:
        model = IndividualOrder
        fields = ("first_name", "contact_method", "recall_me")
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control text-start",
                },
            ),
            "contact_method": forms.Textarea(
                attrs={
                    "style": "height: 60px; width: 100%",
                    "resize": "vertical",
                    "class": "form-control",
                    "id": "contact-method-input",
                    "autocomplete": "tel",
                }
            ),
            "recall_me": forms.CheckboxInput(
                attrs={"id": "recall-me", "class": "form-check-input checkbox-dark"}
            ),
        }

    def save(self, commit=False, user: Optional[User] = None):
        """
        Прикрепляет зарегистрированного пользователя к
        записи индивидуального заказа.

        :param user: Аутентифицированный пользователь, который будет закреплён
        за данным индивидуальным
        """
        order: IndividualOrder = super().save(commit=False)
        if user and user.is_authenticated:
            order.user = user
        order.save(commit)
        return order
