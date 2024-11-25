from dataclasses import dataclass


@dataclass
class RelatedModel:
    """
    A data class to represent a related model and its attributes.

    :param model: The related model name (e.g., 'subcategory', 'subcategory__category').
    :param attributes: A list of attributes for the related model (e.g., ['slug']).
    """

    model: str
    attributes: list[str]
