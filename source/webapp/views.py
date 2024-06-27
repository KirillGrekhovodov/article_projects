from django.shortcuts import render, redirect, get_object_or_404

from webapp.models import Article, Section


def index(request):
    articles = Article.objects.order_by("-created_at")
    return render(request, "index.html", context={"articles": articles})


def create_article(request):
    if request.method == "GET":
        sections = Section.objects.all()
        return render(request, "create_article.html", {"sections": sections})
    else:
        # section = Section.objects.get(pk=request.POST["section_id"])
        article = Article.objects.create(
            title=request.POST.get("title"),
            content=request.POST.get("content"),
            author=request.POST.get("author"),
            section_id=request.POST.get("section_id"),
            #section = section
        )
        return redirect("article_detail", pk=article.pk)


def article_detail(request, *args, pk, **kwargs):
    article = get_object_or_404(Article, pk=pk)
    return render(request, "article_detail.html", context={"article": article})
