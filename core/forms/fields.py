from django.forms import ChoiceField
from phonenumber_field.formfields import REGION_CODE_TO_COUNTRY_CODE


def get_prefix_choices():
    choices = [("", "---------")]
    for region_code, country_code in REGION_CODE_TO_COUNTRY_CODE.items():
        choices.append((region_code, f"{region_code} +{country_code}"))
    return choices


class CountryCodePrefixChoiceField(ChoiceField):
    def __init__(self, *, choices=None, **kwargs):
        if choices is None:
            choices = get_prefix_choices()
            choices.sort(key=lambda item: item[1])
        super().__init__(choices=choices, **kwargs)
