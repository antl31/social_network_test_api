from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from .models import Post, User, PostLike
from .serializers import PostSerializer, UserSerializer, PostLikeSerializer,LikesSerializer

from django_filters.rest_framework import DjangoFilterBackend


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

    def get(self,*args,**kwargs):
        serializer = LikesSerializer
        return Response(serializer.data)

    # like and unlike post
    def create(self, request, *args, **kwargs):
        instance = self.filter_queryset(self.get_queryset())
        post_id = self.request.data['publications']
        PostLike.like_unlike_post(user_id=self.request.user.id, post_id=int(post_id))
        serializer = self.get_serializer(instance, many=True)
        serializer_data = serializer.data  # get the default serialized data
        return Response(serializer_data)

# class PostServiceViewSet(viewsets.ModelViewSet):
#     queryset = PostLike.objects.all()
#     serializer_class = PostLikeSerializer
#     permission_classes = (AllowAny,)
#
#     def create(self, request, *args, **kwargs):
#         instance = self.filter_queryset(self.get_queryset())
#         serializer = self.get_serializer(instance, many=True)
#         serializer_data = serializer.data
#         serializer_data.append({"number_of_likes": int(PostLike.total_likes())})
#         return Response(serializer_data)

class LikesServiceView(viewsets.ModelViewSet):
    serializer_class = PostLikeSerializer
    queryset = PostLike.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter