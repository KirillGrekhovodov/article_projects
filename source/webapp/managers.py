from django.db import models


class ArticlesCommentsManager(models.Manager):
    def with_counts(self):
        return self.annotate(comments_count=models.Count("comments"))

    def with_tags(self):
        return self.filter(tags__isnull=False).distinct()
