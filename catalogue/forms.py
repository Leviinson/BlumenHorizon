from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Bouquet, IndividualQuestion, Product


class BuyItemForm(forms.Form):
    category_slug = forms.SlugField()
    subcategory_slug = forms.SlugField()
    item_slug = forms.SlugField()
    is_bouquet = forms.BooleanField(required=False)


class IndividualQuestionForm(forms.ModelForm):
    item_slug = forms.SlugField(label=_("Идентификатор элемента"))

    class Meta:
        model = IndividualQuestion
        fields = ("contact_method", "item_slug", "recall_me")
        widgets = {
            "contact_method": forms.Textarea(
                attrs={
                    "style": "height: 60px;",
                    "resize": "vertical",
                    "class": "form-control",
                    "id": "contact-method-input",
                    "autocomplete": "tel",
                }
            ),
        }

    def clean_item_slug(self):
        item_slug = self.cleaned_data.get("item_slug")
        try:
            product = Product.objects.get(slug=item_slug, is_active=True)
            self.cleaned_data["related_object"] = product
            self.cleaned_data["related_field"] = "product"
        except Product.DoesNotExist:
            try:
                bouquet = Bouquet.objects.get(slug=item_slug, is_active=True)
                self.cleaned_data["related_object"] = bouquet
                self.cleaned_data["related_field"] = "bouquet"
            except Bouquet.DoesNotExist:
                raise forms.ValidationError(
                    _("Данный продукт был удалён или стал неактивным.")
                )
        return item_slug

    def save(self, commit=False, user=None):
        question: IndividualQuestion = super().save(commit=False)
        if user and user.is_authenticated:
            question.user = user
        related_object = self.cleaned_data.get("related_object")
        related_field = self.cleaned_data.get("related_field")

        if related_object and related_field:
            setattr(question, related_field, related_object)

        question.save(commit)
        return question
