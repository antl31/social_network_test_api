from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Post, User, PostLike
from .filters import F
from .serializers import PostSerializer, UserSerializer, PostLikeSerializer, AggregateSerializer, UserActivitySerializer

from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from rest_framework import mixins


from rest_framework import permissions
class IsAnonCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True

        elif request.user.is_anonymous and request.method != "POST":
            return False
        elif request.method in permissions.SAFE_METHODS:
            return True


class UserViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes =  (IsAnonCreate,)


class PostViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        user = request.user
        user.save()
        super(PostViewSet, self).create(request,*args, **kwargs)

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
        instance = self.filter_queryset(self.get_queryset())
        post_id = self.request.data['publications']
        post_like = PostLike.like_unlike_post(user_id=self.request.user.id, post_id=int(post_id))
        serializer = self.get_serializer(instance, many=True)
        serializer_data = serializer.data  # get the default serialized data
        serializer_data.append({"status": post_like})
        return Response(serializer_data)


class PostServiceViewSet(viewsets.ModelViewSet):
    serializer_class = AggregateSerializer
    model = PostLike
    queryset = PostLike.objects.values('last_updated').annotate(likes=Count('last_updated'))
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


class UserActivityViewSet(viewsets.ModelViewSet):
    serializer_class = UserActivitySerializer
    model = User
    queryset = User.objects.all().values('username', 'last_login', 'last_updated')

    def list(self, request, *args, **kwargs):
        user = request.user
        user.save()
        return super(UserActivityViewSet, self).list(request, *args, **kwargs)





