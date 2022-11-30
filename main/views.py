from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer

User = get_user_model()

@api_view(['GET'])
def post_list(request):
    queryset = Post.objects.all().order_by('id')
    # print("queryset:", queryset)
    serializer = PostSerializer(queryset, many=True)
    # print("serializer.data:", serializer.data)
    return Response(serializer.data, status=200)

@api_view(['POST'])
def create_post(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(status=201)

@api_view(['PATCH'])
def update_post(request, id):
    post = get_object_or_404(Post, id=id)
    serializer = PostSerializer(instance=post, data=request.data, partial=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(status=201)

@api_view(['DELETE'])
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return Response(status=204)

@api_view(['GET'])
def filter_by_user(request, u_id):
    # queryset = Post.objects.filter(author__id=u_id)
    author = get_object_or_404(User, id=u_id)
    queryset = Post.objects.filter(author=author)
    serializer = PostSerializer(queryset, many=True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def search(request):
    q = request.query_params.get('q')
    queryset = Post.objects.filter(body__icontains=q)
    serializer = PostSerializer(queryset, many=True)
    return Response(serializer.data, status=200)
