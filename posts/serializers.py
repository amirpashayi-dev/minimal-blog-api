from rest_framework import serializers
from .models import Post, PostLike
from accounts.models import User, Follow
from comments.models import Comment


class PostSerializer(serializers.ModelSerializer):
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        exclude = ('user',)

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return Post.objects.create(**validated_data)

    def get_comments_count(self, obj):
        return Comment.objects.filter(post=obj, is_approved=True).count()

    def get_likes_count(self, obj):
        return PostLike.objects.filter(post=obj, value='like').count()


class AuthorSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('full_name', 'age', 'bio', 'email')

    def get_followers_count(self, obj):
        return Follow.objects.filter(to_user=obj).count()


class AuthorPostsSerializer(serializers.Serializer):
    posts = PostSerializer(many=True)
    author = AuthorSerializer()