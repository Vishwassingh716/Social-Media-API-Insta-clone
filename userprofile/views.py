from django.shortcuts import render
from django.contrib.auth import login,logout
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework import generics,status
from rest_framework.permissions import IsAdminUser,AllowAny,IsAuthenticated
from rest_framework.views import APIView 
from rest_framework.authentication import SessionAuthentication
from django.views.decorators.csrf import csrf_exempt
from rest_framework import mixins
from django.core.exceptions import ObjectDoesNotExist

class UserList(generics.ListCreateAPIView):
    queryset = ProfilePage.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminUser]

    def list(self, request):
        queryset = self.get_queryset()
        serializer = ProfileSerializer(queryset, many=True)
        return Response(serializer.data)
        


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        cleaned_data = request.data
        serializer = UserRegistrationSerializer(data= cleaned_data)
        if serializer.is_valid(raise_exception=True):
            user_obj = serializer.create(cleaned_data)

            profile = ProfilePage(User = user_obj , name = user_obj.username)
            

            if user_obj:
                profile.save()
                return Response(serializer.data , status = status.HTTP_201_CREATED)
            
        return Response(status = status.HTTP_400_BAD_REQUEST)



class UserLoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [SessionAuthentication]

    def post(self,request):
        data = request.data
        serializer = UserLoginSerializer(data = data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(data)
            login(request,user)
            return Response(serializer.data , status = status.HTTP_200_OK)
        return Response(status = status.HTTP_400_BAD_REQUEST)

class UserLogoutView(APIView):
    def post(self,request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
    


class RetrieveUserView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ProfilePage.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        try:
            user = User.objects.get(id = self.kwargs['pk'])
        except ObjectDoesNotExist:
            return None

        else:
            return queryset.get(User = user)
    
    def get(self,request,pk):
        queryset = self.get_queryset()
        if queryset is None:
            return Response("user not found" , status = status.HTTP_404_NOT_FOUND)
        serializer = ProfileSerializer(queryset)
        return Response(serializer.data)
    
    def put(self,request,pk):
        queryset = self.get_queryset()
        if queryset is None:
            return Response("user not found" , status = status.HTTP_404_NOT_FOUND)
        if queryset.User!= self.request.user:
            return Response("you are not allowed to update this profile")
        serializer = ProfileSerializer(queryset,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)



class PostsView(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Posts.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



class RetrievePostView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Posts.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset=  super().get_queryset()
        try:
            post = Posts.objects.get(id = self.kwargs['pk'])
        except ObjectDoesNotExist:
            return None
        else:
            return post
    
    def get(self,request,pk):
        queryset = self.get_queryset()
        if queryset is None:
            return Response("post does not exist" , status=status.HTTP_404_NOT_FOUND)
        queryset.uploader = self.request.user
        serializer= PostSerializer(queryset)
        return Response(serializer.data)
        
    def put(self,request,pk):
        queryset = self.get_queryset()
        if queryset is None:
            return Response("post does not exist" , status=status.HTTP_404_NOT_FOUND)
        if queryset.uploader!=self.request.user:
            return Response("you are not allowed to update this post")

        serializer= PostSerializer(queryset , data = request.data , partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self,request,pk):
        queryset = self.get_queryset()
        if queryset is None:
            return Response("post does not exist" , status=status.HTTP_404_NOT_FOUND)
        if queryset.uploader!=self.request.user:
            return Response("you are not allowed to delete this post")
        queryset.delete()
        return Response("post deleted")



class UserPostView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Posts.objects.all()
    serializer_class = UserPostSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = User.objects.get(id = self.kwargs['pk'])
        return queryset.filter(uploader = user)

    def list (self,*args,**kwargs):
        queryset = self.get_queryset()
        serializer = UserPostSerializer(queryset,many=True)
        return Response(serializer.data)
    
class LikePostView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    serializer_class = PostSerializer

    def get(self,request,pk):
        try:
            posted = Posts.objects.get(id = pk)
            liking_post = LikePost.objects.get_or_create(user = self.request.user , post = posted)
            if not liking_post[1]:
                posted.no_of_likes-=1
                liking_post[0].delete()
                serializer = PostSerializer(posted , data = request.data , partial = True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors)
            else:
                posted.no_of_likes+=1
                serializer = PostSerializer(posted , data = request.data , partial = True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors)

        except ObjectDoesNotExist:
            return Response("post does not exist" , status=status.HTTP_404_NOT_FOUND)


class RetrieveUserswholikedView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = LikePost.objects.all()
    serializer_class = LikedPostSerializer

    def get_queryset(self):
        queryset =  super().get_queryset()
        post = Posts.objects.get(id = self.kwargs['pk'])
        return queryset.filter(post = post)
    
    def list (self,*args,**kwargs):
        queryset = self.get_queryset()
        serializer = LikedPostSerializer(queryset,many=True)
        return Response(serializer.data)
    
class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    serializer_class = FollowUserSerializer
    queryset = Followers.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        user = User.objects.get(id = self.kwargs['pk'])
        return queryset.filter(user = user)
    
    def post(self,request,pk):
        try:
            user = User.objects.get(id = pk)
            follows = Followers.objects.get_or_create(user = user , follower = request.user)
            if not follows[1]:
                profile = ProfilePage.objects.get(User = user)
                profile.no_of_followers-=1
                profile.save()
                follows[0].delete()
                serializer = ProfileSerializer(profile , data = request.data , partial = True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
            else:
                profile = ProfilePage.objects.get(User = user)
                profile.no_of_followers+=1
                profile.save()

                serializer = ProfileSerializer(profile , data = request.data , partial = True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response("user not found" ,status= status.HTTP_404_NOT_FOUND)
        
class RetrieveUserWhoFollowView(generics.ListAPIView):
    serializer_class = FollowUserSerializer
    permission_classes = [IsAuthenticated]
    queryset = Followers.objects.all()

    def get_queryset(self):
        queryset =  super().get_queryset()
        user = User.objects.get(id = self.kwargs['pk'])
        return queryset.filter(user = user)
    
    def list(self,*args,**kwargs):
        queryset = self.get_queryset()
        serializer = RetrieveFollowUserSerializer(queryset , many = True)
        return Response(serializer.data)
    
class CommentsView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CommentOnPost.objects.all()
    serializer_class = CommentSerializer


    
    def post(self,request,pk):
        try:
            post = Posts.objects.get(id = pk)
            comments = CommentOnPost.objects.create(user = request.user , post = post)
            serializer = CommentSerializer(comments, data = request.data,partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data , status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors)
        
        except ObjectDoesNotExist:
            return Response("post not found" , status=status.HTTP_404_NOT_FOUND)

class RetrieveCommentView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CommentOnPost.objects.all()
    serializer_class = RetrieveCommentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        post = Posts.objects.get(id = self.kwargs["pk"]) 
        return queryset.filter(post = post)
    def list(self,*args,**kwargs):
        queryset = self.get_queryset()
        Serializer = RetrieveCommentSerializer(queryset , many = True)
        return Response(Serializer.data)
    
class DeleteCommentView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CommentOnPost.objects.all()
    serializer_class = RetrieveCommentSerializer

    def destroy(self, request, pk):
        try:
            comment = CommentOnPost.objects.get(id = pk)
            if comment.user == request.user:
                self.perform_destroy(comment)
                return Response("comment deleted")
            else:
                return Response("you are not authorized to delete this comment")
        
        except ObjectDoesNotExist:
            return Response("comment does not exist")

    
