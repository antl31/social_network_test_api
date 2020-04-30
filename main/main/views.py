from rest_framework import viewsets
from rest_framework import generics
from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from .models import Post, User, PostLike
from .serializers import PostSerializer, UserSerializer, PostLikeSerializer, AggregateSerializer
from django.db.models import Q
from datetime import datetime
from django.db.models import Count, Sum


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
    # queryset = PostLike.objects.annotate(likes= Count('publications_id')).values('likes','last_updated',).order_by('last_updated',)
    queryset = PostLike.objects.values('last_updated').annotate(likes=Count('last_updated'))
    # def list(self, request, *args, **kwargs):
    #     if request.query_params.get('date_from', None) and request.query_params.get('date_to', None):
    #         quryset_data = {'last_updated_before': request.query_params['date_to'],
    #                         'last_updated_after': request.query_params['date_from']}
    #         serializer = PostLikeSerializer(F(quryset_data).qs, many=True)
    #     elif request.query_params.get('date_from', None):
    #         quryset_data = {'last_updated_after': request.query_params['date_from']}
    #         serializer = PostLikeSerializer(F(quryset_data).qs, many=True)
    #     elif request.query_params.get('date_to', None):
    #         quryset_data = {'last_updated_before': request.query_params['date_to']}
    #         serializer = PostLikeSerializer(F(quryset_data).qs, many=True)
    #     else:
    #         serializer = PostLikeSerializer(self.get_queryset(), many=True)
    #     return Response(serializer.data)
