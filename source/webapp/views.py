from django.shortcuts import render, redirect, get_object_or_404

from webapp.forms import ArticleForm
from webapp.models import Article


def index(request):
    articles = Article.objects.order_by("-created_at")
    return render(request, "index.html", context={"articles": articles})


def create_article(request):
    if request.method == "GET":
        form = ArticleForm()
        return render(request, "create_article.html", {"form": form})
    else:
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article = form.save()
            return redirect("article_detail", pk=article.pk)

        return render(
            request,
            "create_article.html",
            {"form": form}
        )


def article_detail(request, *args, pk, **kwargs):
    article = get_object_or_404(Article, pk=pk)
    return render(request, "article_detail.html", context={"article": article})


def update_article(request, *args, pk, **kwargs):
    if request.method == "GET":
        article = get_object_or_404(Article, pk=pk)
        form = ArticleForm(instance=article)
        return render(
            request, "update_article.html",
            context={"form": form}
        )
    else:
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article = form.save()
            return redirect("article_detail", pk=article.pk)
        else:
            return render(
                request,
                "update_article.html",
                {"form": form}
            )


def delete_article(request, *args, pk, **kwargs):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "GET":
        return render(request, "delete_article.html", context={"article": article})
    else:
        article.delete()
        return redirect("articles")
