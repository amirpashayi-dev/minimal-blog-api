from rest_framework import serializers
from .models import Post
from accounts.models import User
from comments.models import Comment


class PostSerializer(serializers.ModelSerializer):
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        exclude = ('user',)

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return Post.objects.create(**validated_data)

    def get_comments_count(self, obj):
        return Comment.objects.filter(post=obj, is_approved=True).count()


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('full_name', 'age', 'bio', 'email')


class AuthorPostsSerializer(serializers.Serializer):
    posts = PostSerializer(many=True)
    author = AuthorSerializer()