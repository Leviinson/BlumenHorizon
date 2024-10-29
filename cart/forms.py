from django import forms


class ProductForm(forms.Form):
    product_or_bouquet_slug = forms.SlugField()
    is_bouquet = forms.BooleanField()