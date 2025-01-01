"""
Данный модуль служит для хранения функций, которые используются хотя-бы
два раза в разных приложениях.

Если отдельная функция используется несколько раз внутри одного приложения,
но в разных модулях - то её следует поместить в собственной папке services/utils
внутри данного приложения.
"""

from .carts import get_carts
from .recommended_items import get_recommended_items_with_first_image
from .urls import build_absolute_uri
