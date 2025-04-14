from rest_framework import serializers, validators
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'text', 'pub_date', 'author', 'image', 'group', )
        read_only_fields = ('author', 'id', 'pub_date', 'image',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created',)
        read_only_fields = ('author', 'id', 'created', 'post')


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(slug_field='username',
                                             queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ('user', 'following',)
        read_only_fields = ('user',)
        validators = [
            validators.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='Its not allowed to follow somebody twice!'
            )
        ]

    def validate_following(self, value):
        user = self.context.get('request').user
        if value == user:
            raise serializers.ValidationError(
                'Its not allowed to follow yourself!'
            )
        return value


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description',)
        read_only_fields = ('id', 'slug', 'description')
