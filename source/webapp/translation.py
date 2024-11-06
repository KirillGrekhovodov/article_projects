from modeltranslation.translator import translator, TranslationOptions
from webapp.models import Article


class ArticleTranslationOptions(TranslationOptions):
    fields = ('title',)


translator.register(Article, ArticleTranslationOptions)
