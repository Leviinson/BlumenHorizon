from dataclasses import dataclass
from typing import Literal


@dataclass
class CartAction:
    action: Literal["add", "remove", "remove_single"]
