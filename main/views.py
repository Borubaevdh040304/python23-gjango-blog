from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer


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
