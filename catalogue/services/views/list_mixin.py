from typing import Any


class ListViewMixin:
    allow_empty = True
    paginate_by = 9

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(self, *args, **kwargs)
        return context
