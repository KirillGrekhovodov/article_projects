from datetime import datetime

from django.core.management.base import BaseCommand

from webapp.models import Article


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument(
            "--date",
            type=str,
            help="Delete poll instead of closing it",
        )

    def handle(self, *args, **options):
        user_date_str = options.get("date")
        if user_date_str:
            user_date = datetime.strptime(user_date_str, "%Y-%m-%d")
            articles = Article.objects.filter(created_at__lt=user_date)
            articles.delete()
