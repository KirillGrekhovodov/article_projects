from rest_framework import serializers

from webapp.models import Tag, Comment
from webapp.models.article import Article


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', ]


class ArticleSerializer(serializers.ModelSerializer):
    tags = serializers.ListSerializer(child=serializers.CharField(max_length=100), required=False)

    # tags_read = TagSerializer(many=True, read_only=True, source='tags')

    def save(self, **kwargs):
        tags = self.validated_data.pop('tags', [])
        article = super().save(**kwargs)
        if tags:
            tags_objects = []
            for tag_name in tags:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                tags_objects.append(tag)
            article.tags.set(tags_objects)
        return article


    def validate(self, attrs):
        return super().validate(attrs)

    def validate_title(self, value):
        # print(self.context["request"])
        if len(value) < 5:
            raise serializers.ValidationError("Длина додлжна быть больше пяти")
        return value

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["tags"] = TagSerializer(instance.tags.all(), many=True).data
        return data

    class Meta:
        model = Article
        fields = ["id", "title", "content", "status", "tags", "created_at", "updated_at", "author", ]
        read_only_fields = ["id", "created_at", "updated_at"]


class ArticleShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["id", "title"]
        read_only_fields = fields
