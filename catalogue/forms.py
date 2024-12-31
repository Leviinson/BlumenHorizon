from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Bouquet, IndividualQuestion, Product


class BuyItemForm(forms.Form):
    category_slug = forms.SlugField()
    subcategory_slug = forms.SlugField()
    item_slug = forms.SlugField()
    is_bouquet = forms.BooleanField(required=False)


class IndividualQuestionForm(forms.ModelForm):
    """
    Форма для отправки индивидуального вопроса
    с привязкой к «стандартному товару» или букету.
    """

    item_slug = forms.SlugField(label="Идентификатор элемента")

    class Meta:
        model = IndividualQuestion
        fields = ("contact_method", "item_slug", "recall_me")
        widgets = {
            "contact_method": forms.Textarea(
                attrs={
                    "style": "height: 60px;",
                    "resize": "vertical",
                    "class": "form-control",
                    "id": "contact-method-input",
                    "autocomplete": "tel",
                }
            ),
            "recall_me": forms.CheckboxInput(
                attrs={"id": "recall-me", "class": "form-check-input checkbox-dark"}
            ),
        }

    def clean_item_slug(self):
        """
        Валидация поля item_slug.

        Проверяет, существует ли активный продукт или букет с указанным slug.
        Если найден, сохраняет объект и тип объекта в cleaned_data.

        Returns:
            str: Валидный slug элемента.

        Raises:
            forms.ValidationError: Если продукт или букет не найден или неактивен.
        """
        item_slug = self.cleaned_data.get("item_slug")
        product = self._get_active_product(item_slug)
        if product:
            self._set_related_data(product, "product")
        else:
            bouquet = self._get_active_bouquet(item_slug)
            if bouquet:
                self._set_related_data(bouquet, "bouquet")
            else:
                raise forms.ValidationError(
                    _("Данный продукт был удалён или стал неактивным.")
                )
        return item_slug

    def save(self, commit=False, user=None):
        question: IndividualQuestion = super().save(commit=False)
        if user and user.is_authenticated:
            question.user = user
        related_object = self.cleaned_data.get("related_object")
        related_field = self.cleaned_data.get("related_field")

        if related_object and related_field:
            setattr(question, related_field, related_object)

        question.save(commit)
        return question

    def _get_active_product(self, slug):
        """
        Получает активный «стандартный товар» по slug.

        Args:
            slug (str): Идентификатор продукта.

        Returns:
            Product | None: Найденный продукт или None.
        """
        try:
            return Product.objects.only("pk").get(slug=slug, is_active=True)
        except Product.DoesNotExist:
            return None

    def _get_active_bouquet(self, slug):
        """
        Получает активный букет по slug.

        Args:
            slug (str): Идентификатор букета.

        Returns:
            Bouquet | None: Найденный букет или None.
        """
        try:
            return Bouquet.objects.only("pk").get(slug=slug, is_active=True)
        except Bouquet.DoesNotExist:
            return None

    def _set_related_data(self, related_object, related_field):
        """
        Устанавливает связанные данные в cleaned_data.

        Args:
            related_object (Model): Найденный объект.
            related_field (str): Поле, связанное с объектом.
        """
        self.cleaned_data["related_object"] = related_object
        self.cleaned_data["related_field"] = related_field

    def _prepare_question(self, commit, user):
        """
        Создаёт без сохранения и заполняет объект IndividualQuestion.

        Args:
            commit (bool): Флаг сохранения объекта в базу.
            user (User): Пользователь, связанный с вопросом.

        Returns:
            IndividualQuestion: Экземпляр модели с заполненными данными.
        """
        question = super().save(commit=False)
        if user and user.is_authenticated:
            question.user = user
        return question

    def _link_related_object(self, question):
        """
        Привязывает объект («стандартный товар» или букет) к вопросу.

        Args:
            question (IndividualQuestion): Экземпляр вопроса, к которому нужно привязать объект.
        """
        related_object = self.cleaned_data.get("related_object")
        related_field = self.cleaned_data.get("related_field")
        if related_object and related_field:
            setattr(question, related_field, related_object)
