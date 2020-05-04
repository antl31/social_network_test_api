from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Post, PostLike

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', "last_name", 'last_updated', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        read_only_fields = ('author',)
        fields = (
            'author',
            'title',
            'text',
            'created_date',
        )


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        read_only_fields = ('user',)
        fields = (
            'user',
            'publications',
            'last_updated'
        )


class AggregateSerializer(serializers.Serializer):
    likes = serializers.IntegerField()
    last_updated = serializers.DateField()

    class Meta:
        model = PostLike
        read_only_fields = ('user',)
        fields = (
            'user',
            'publications',
            'last_updated'
        )


class UserActivitySerializer(serializers.Serializer):
    username = serializers.CharField()
    last_login = serializers.DateTimeField()
    last_updated = serializers.DateTimeField()

    class Meta:
        model = User
        fields = (
            'last_login',
            'last_updated'
        )