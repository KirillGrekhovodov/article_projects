import string
from random import choice

from django.db import models
from uuslug import uuslug

statuses = [("new", "Новая"), ("moderated", "Модерированная"), ("deleted", "Удаленная")]


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(choice(chars) for _ in range(size))


def unique_slug_generator(article, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = uuslug(article.title, article)
    max_length = 20
    slug = slug[:max_length]
    qs_exists = Article.objects.filter(slug=slug).exists()

    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug[:max_length - 5], randstr=random_string_generator(size=4))
        return unique_slug_generator(article, new_slug=new_slug)
    return slug


class Section(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name="Название", unique=True)
    description = models.CharField(max_length=50, null=True, blank=True, verbose_name="Описание")

    def __str__(self):
        return f"{self.pk}. {self.title}"

    class Meta:
        db_table = "sections"
        verbose_name = "Секция"
        verbose_name_plural = "Секции"


class Article(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name="Название", unique=True)
    author = models.CharField(max_length=50, null=False, blank=False, verbose_name="Автор", default="Неизвестный")
    content = models.TextField(null=False, blank=False, verbose_name="Контент")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")
    status = models.CharField(max_length=20, choices=statuses, verbose_name="Статус", default=statuses[0][0])
    section = models.ForeignKey(
        "webapp.Section",
        on_delete=models.RESTRICT,
        verbose_name="Секция",
        related_name="articles",  # article_set,
    )
    publish_date = models.DateField(verbose_name="Дата публикации", null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.pk}. {self.title}: {self.author}"

    class Meta:
        db_table = "articles"
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
