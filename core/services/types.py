from typing import NewType

RelativeUrl = NewType("RelativeUrl", str)
AbsoluteUrl = NewType("AbsoluteUrl", str)

# По какому полю сортировать queryset
OrderedModelField = NewType("OrderedModelField", str)

Limit = NewType("Limit", int)
