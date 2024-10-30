from django import forms


class CartForm(forms.Form):
    product_slug = forms.SlugField()
