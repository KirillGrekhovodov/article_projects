from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from django.utils.translation import gettext_lazy as _

from webapp.models import Article


def title_validate(title):
    min_length = 5
    if len(title) < min_length:
        message = _("forms.articles.title_validate: Title must be at least %(min_length)s characters long.")
        raise ValidationError(message, params={'min_length': min_length})

class ArticleForm(forms.ModelForm):
    title_ru = forms.CharField(max_length=50, required=True, label=_("models.article.title: title"), validators=[title_validate])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for v in self.visible_fields():
            if not isinstance(v.field.widget, widgets.CheckboxSelectMultiple):
                v.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Article
        fields = ("title_ru", "title_en", "content", "tags")
        widgets = {"tags": widgets.CheckboxSelectMultiple()}


