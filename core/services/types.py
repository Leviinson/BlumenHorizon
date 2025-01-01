from typing import NewType

RelativeUri = NewType("RelativeUri", str)
AbsoluteUri = NewType("AbsoluteUri", str)

# По какому полю сортировать queryset
OrderedModelField = NewType("OrderedModelField", str)

Limit = NewType("Limit", int)
