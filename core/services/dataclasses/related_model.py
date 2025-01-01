from dataclasses import dataclass


@dataclass
class RelatedModel:
    """
    A data class to represent a related model and its attributes.

    :param model: The related model name (e.g., 'subcategory', 'subcategory__category').
    :param fields: A list of fields of the related model (e.g., ['slug']).
    """

    model: str
    fields: list[str]
