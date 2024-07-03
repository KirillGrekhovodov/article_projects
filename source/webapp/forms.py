from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets
from webapp.models import Article


class ArticleForm(forms.ModelForm):
    # title = forms.CharField(
    #         max_length=30,
    #         required=True,
    #         label="Название",
    #         error_messages={
    #             "required": "Это поле обязательное"
    #         })

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

    class Meta:
        model = Article
        fields = ['title', 'author', 'content', 'publish_date', 'status', 'section']
        error_messages = {
            "title": {
                "required": "Поле обязательное"
            }
        }
        widgets = {
            'content': widgets.Textarea(attrs={'cols': 20, "rows": 5}),
            'publish_date': widgets.DateInput(attrs={"type": "date"}),
        }




