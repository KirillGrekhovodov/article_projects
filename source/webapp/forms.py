from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.forms import widgets
from webapp.models import statuses as STATUSES_CHOICES, Section


# def publish_date_validate(publish_date):
#     if publish_date < date.today():
#         raise ValidationError("Дата публикации не может быть раньше чем сегодня")


class ArticleForm(forms.Form):
    title = forms.CharField(
        max_length=30,
        required=True,
        label="Название",
        error_messages={
            "required": "Это поле обязательное"
        })
    author = forms.CharField(
        max_length=50,
        required=False,
        label="Автор",
        initial="Неизвестный",
        widget=widgets.Input(attrs={"placeholder": "Автор"}),
    )
    content = forms.CharField(
        max_length=3000,
        required=True,
        label="Контент",
        widget=widgets.Textarea(attrs={"cols": 20, "rows": 5, "placeholder": "Контент"}),
        validators=[]
    )
    status = forms.ChoiceField(choices=STATUSES_CHOICES, label="Статус", required=False)
    section = forms.ModelChoiceField(queryset=Section.objects.all(), label="Секция")
    publish_date = forms.DateField(
        label="Дата публикации",
        required=False,
        widget=widgets.DateInput(attrs={"type": "date"}),
        # validators=[publish_date_validate, ]
    )

    def clean_publish_date(self):
        publish_date = self.cleaned_data["publish_date"]
        if publish_date and publish_date < date.today():
            raise ValidationError("Дата публикации не может быть раньше чем сегодня")
        return publish_date

    def clean(self):
        title = self.cleaned_data.get("title")
        content = self.cleaned_data.get("content")
        if title and content and title == content:
            raise ValidationError("Название и контент не могут быть равны")
        return super().clean()
