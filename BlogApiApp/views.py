from django.shortcuts import render
#we import these two libraries to create api endpoints 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . models import Post
from . serializers import PostSerializer
# Create your views here.

#the list takes in the type of request the endpoint will use 
@api_view(['GET'])
def index(request):

    return Response({"Success":"The api setup was successful"})

@api_view(['GET'])
def get_all_posts(request):
    get_posts = Post.objects.all()
    serializer_class = PostSerializer(get_posts, many= True)
    
    return Response(serializer_class.data)

# we use get and post cuz we would be creating a post 
@api_view(['GET','POST'])
def create_post(request):
    #this time we are getting the data submitted by the client
    data = request.data 
    # checking if the data submitted by the user is valid 
    serializer_class = PostSerializer(data = data)
    if serializer_class.is_valid():
        #Then saving it to the DB if valid 
        serializer_class.save()
        # then return a response to the let the client know the post has been created 
        return Response({"Success":"Your Post has been created successfully"}, status=201)
    else:
        #serializer_class.errors handles the error message 
        return Response(serializer_class.errors, status=400)

@api_view(['DELETE'])
def delete_post(request):
    # first get the Id of the post we want to delete from the user using command below 
    post_id = request.data.get('post_id')
    # check if the post most exist in The DB by matching the ID 
    try:
        post = Post.objects.get(id = post_id)
        post.delete()
        return Response({"Success":"This Post has been deleted successfully"}, status=201)
    # if it does not exist only 
    except Post.DoesNotExist:
        return Response({"Error":"This Post Does Not Exist"}, status=404)
    
# get a particular blog post 
@api_view(['GET'])
def get_post(request):
    post_id = request.data.get('post_id')
    try:
        post = Post.objects.get(id = post_id)
        #after getting the post by the Id , we then serialize it with serializer class and many is not true cuz we are getting only one item
        serializer_class = PostSerializer(post)
        return Response(serializer_class.data)
    # if it does not exist only 
    except Post.DoesNotExist:
        return Response({"Error":"This Post Does Not Exist"}, status=404)

#Update Post   
@api_view(['PUT'])
def update_post(request):
    post_id = request.data.get('post_id')
    title = request.data.get('title')
    content = request.data.get('content')
    
    try:
        post = Post.objects.get(id = post_id)
        if title:
            post.title = title
        if content:
            post.content = content
        post.save()
        return Response({"Success":"Your Post Was Updated Successfully"}, status=200)
    except Post.DoesNotExist:
        return Response({"Error":"This Post Does Not Exist"}, status=404)


    



    
    