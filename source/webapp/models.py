from django.db import models

statuses = [("new", "Новая"), ("moderated", "Модерированная"), ("deleted", "Удаленная")]


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
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name="Название")
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

    def __str__(self):
        return f"{self.pk}. {self.title}: {self.author}"

    class Meta:
        db_table = "articles"
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
