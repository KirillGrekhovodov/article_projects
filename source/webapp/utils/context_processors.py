from webapp.models import Tag


def add_tags(request):
    return {"tags": Tag.objects.all()}
