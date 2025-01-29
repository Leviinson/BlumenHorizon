from typing import TypedDict


class AvgRating(TypedDict):
    value: float
    range: range
    fractional_gte_5: bool
    count: int
