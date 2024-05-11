from django.forms import ValidationError
from rest_framework.serializers import ModelSerializer,Serializer
from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model , authenticate


UserModel = get_user_model()

class ProfileSerializer(ModelSerializer):
    class Meta:
        model = ProfilePage
        fields = "__all__"



class UserRegistrationSerializer(ModelSerializer):
    class Meta:
        model = UserModel
        fields = "__all__"

    def create(self, validated_data):
        user_obj = UserModel.objects.create_user(username=validated_data['username'],password = validated_data['password'])
        user_obj.save()
        return user_obj



class UserLoginSerializer(Serializer):
    usernameser = serializers.CharField()
    passwordser = serializers.CharField()
    
    def check_user(self,validated_data):
         user = authenticate(username = validated_data['usernameser'] , password = validated_data['passwordser'])

         if not user:
             raise ValidationError('user not found')
         
         return user
    
class PostSerializer(ModelSerializer):
    class Meta:
        model = Posts
        fields = "__all__"
    
    caption = serializers.CharField(default=...) 
    uploader = serializers.HiddenField(default = serializers.CurrentUserDefault())
    no_of_likes = serializers.ReadOnlyField()

class UserPostSerializer(ModelSerializer):
    class Meta:
        model = Posts
        fields = "__all__"


class LikedPostSerializer(ModelSerializer):
    class Meta:
        model = LikePost
        fields = "__all__"


class FollowUserSerializer(ModelSerializer):
    class Meta:
        model = Followers
        fields = "__all__"
    
    user = serializers.ReadOnlyField()
    follower = serializers.HiddenField(default = serializers.CurrentUserDefault())


class RetrieveFollowUserSerializer(ModelSerializer):
    class Meta:
        model = Followers
        fields = "__all__"

class CommentSerializer(ModelSerializer):
    class Meta:
        model = CommentOnPost
        fields = "__all__"

    user = serializers.HiddenField(default = serializers.CurrentUserDefault())
    post = serializers.PrimaryKeyRelatedField(read_only= True)
    description = serializers.CharField(default = ...)
    

class RetrieveCommentSerializer(ModelSerializer):
    class Meta:
        model = CommentOnPost
        fields = "__all__"