from rest_framework import serializers
from .models import Post, Category, Tag


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]


class PostListSerializer(serializers.ModelSerializer):
    """Lightweight — used for homepage / listing / search results."""
    author_name = serializers.CharField(source="author.get_full_name", read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    reading_time = serializers.IntegerField(source="reading_time_minutes", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id", "title", "slug", "excerpt", "featured_image",
            "author_name", "category", "tags",
            "published_at", "reading_time",
        ]


class PostDetailSerializer(PostListSerializer):
    class Meta(PostListSerializer.Meta):
        fields = PostListSerializer.Meta.fields + [
            "content", "meta_description", "updated_at",
        ]


class AuthorPostSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    reading_time = serializers.IntegerField(source="reading_time_minutes", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id", "title", "slug", "excerpt", "content", "featured_image",
            "category", "tags", "status", "published_at", "updated_at",
            "reading_time",
        ]


class AuthorPostWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field="slug", queryset=Category.objects.all(), required=False, allow_null=True)
    tags = serializers.ListField(child=serializers.CharField(), required=False, write_only=True)

    class Meta:
        model = Post
        fields = [
            "id", "title", "slug", "excerpt", "content", "featured_image",
            "category", "tags", "status", "meta_description",
        ]

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        tags = validated_data.pop("tags", [])
        post = super().create(validated_data)
        post.tags.set(self._get_or_create_tags(tags))
        return post

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", None)
        post = super().update(instance, validated_data)
        if tags is not None:
            post.tags.set(self._get_or_create_tags(tags))
        return post

    def _get_or_create_tags(self, tag_names):
        tag_objects = []
        for tag_name in tag_names:
            tag_name = tag_name.strip()
            if not tag_name:
                continue

            existing_tag = Tag.objects.filter(name__iexact=tag_name).first()
            if existing_tag:
                tag_objects.append(existing_tag)
                continue

            slug = tag_name.lower().replace(" ", "-")
            base_slug = slug
            counter = 1
            while Tag.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            tag = Tag.objects.create(name=tag_name, slug=slug)
            tag_objects.append(tag)
        return tag_objects
