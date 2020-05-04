from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins

from .models import Post, User, PostLike
from .filters import DateFilter
from .serializers import PostSerializer, UserSerializer, PostLikeSerializer, AggregateSerializer, UserActivitySerializer
from .permissions import IsAnonCreate


class UserViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAnonCreate,)


class PostViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        user = self.request.user
        user.save()
        serializer.save(author=self.request.user)

    def list(self, request, *args, **kwargs):
        user = request.user
        user.save()
        return super(PostViewSet, self).list(request, *args, **kwargs)


class PostLikeViewSet(mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        user = request.user
        user.save()
        post_id = self.request.data['publications']
        PostLike.like_unlike_post(user_id=self.request.user.id, post_id=int(post_id))
        super(PostLikeViewSet, self).create(request, *args, **kwargs)


class PostServiceViewSet(mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = AggregateSerializer
    model = PostLike
    queryset = PostLike.objects.values('last_updated').annotate(likes=Count('last_updated'))
    filter_backends = [DjangoFilterBackend]
    filter_class = DateFilter

    def list(self, request, *args, **kwargs):
        user = request.user
        user.save()
        return super(PostServiceViewSet, self).list(request, *args, **kwargs)


class UserActivityViewSet(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = UserActivitySerializer
    model = User
    queryset = User.objects.all().values('username', 'last_login', 'last_updated')

    def list(self, request, *args, **kwargs):
        user = request.user
        user.save()
        return super(UserActivityViewSet, self).list(request, *args, **kwargs)
