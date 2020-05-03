from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Post, User, PostLike
from .filters import F
from .serializers import PostSerializer, UserSerializer, PostLikeSerializer, AggregateSerializer,UserActivitySerializer

from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostLikeViewSet(viewsets.ModelViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        instance = self.filter_queryset(self.get_queryset())
        post_id = self.request.data['publications']
        post_like = PostLike.like_unlike_post(user_id=self.request.user.id, post_id=int(post_id))
        serializer = self.get_serializer(instance, many=True)
        serializer_data = serializer.data  # get the default serialized data
        serializer_data.append({"status": post_like})
        # request.data['status'] = post_like
        return Response(serializer_data)


class PostServiceViewSet(viewsets.ModelViewSet):
    serializer_class = AggregateSerializer
    model = PostLike
    queryset = PostLike.objects.values('last_updated').filter(last_updated__gte='2020-04-28').annotate(likes=Count('last_updated'))
    filter_backends = [DjangoFilterBackend]
    filter_class = F

    def create(self, request, *args, **kwargs):
        user = request.user
        user.save()
        super(PostServiceViewSet, self).create(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        user = request.user
        user.save()
        return super(PostServiceViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        user.save()
        super(PostServiceViewSet, self).retrieve(request,*args, **kwargs)


class UserActivityViewSet(viewsets.ModelViewSet):
    serializer_class = UserActivitySerializer
    model = User
    queryset = User.objects.all().values('username', 'last_login', 'last_updated')

    def list(self, request, *args, **kwargs):
        user = request.user
        user.save()
        return super(UserActivityViewSet, self).list(request, *args, **kwargs)





