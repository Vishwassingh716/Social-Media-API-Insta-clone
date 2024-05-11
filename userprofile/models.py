from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ProfilePage(models.Model):
    User = models.OneToOneField(User, on_delete = models.CASCADE)
    name = models.CharField(max_length = 30,null = True)
    email = models.EmailField(max_length = 256, null = True,unique=True)
    profilephoto = models.ImageField(upload_to='images/',null = True , blank = True ,default = "default.jpg")
    no_of_followers = models.IntegerField(default = 0,null = True)
    no_of_following = models.IntegerField(default = 0,null = True)
    no_of_posts = models.IntegerField(default = 0,null = True)
    bio = models.CharField(max_length = 200 , null = True)

    def __str__(self):
        return self.name
    
        
class Posts(models.Model):
    uploader = models.ForeignKey(User,null = True , on_delete = models.CASCADE)
    img = models.ImageField(upload_to = 'images/',null = True)
    caption = models.CharField(max_length = 400 , null = True)
    time = models.DateTimeField(auto_now_add = True)
    Like = models.BooleanField(default = False)
    no_of_likes = models.IntegerField(default = 0)
    #comment
    def __str__(self):
        return self.caption
    
class LikePost(models.Model):
    user = models.ForeignKey(User,null = True ,on_delete = models.CASCADE)
    post = models.ForeignKey(Posts ,null = True ,on_delete = models.CASCADE)

    class Meta:
        unique_together = ('user','post')

class CommentOnPost(models.Model):
    user = models.ForeignKey(User, null = True , on_delete = models.CASCADE)
    post = models.ForeignKey(Posts,null = True , on_delete = models.CASCADE)
    description = models.CharField(max_length = 400, default = "commented")
    time = models.DateTimeField(auto_now_add = True)

    class Meta:
        unique_together = ('user','post','time')

# class LikeOnComment(models.Model):
#     user = models.ForeignKey(ProfilePage,null = True,on_delete = models.CASCADE )
#     comment = models.ForeignKey(CommentOnPost , null = True,on_delete = models.CASCADE)

#     class Meta:
#         unique_together = ('user','comment')


# class ReplyOncomment(models.Model):
#     user = models.ForeignKey(ProfilePage, null = True , on_delete = models.SET_NULL)
#     comment = models.ForeignKey(CommentOnPost,null = True , on_delete = models.SET_NULL)
#     description = models.CharField(max_length = 400,null = True)
#     time = models.DateTimeField(auto_now_add = True)
#     like = models.BooleanField(default = False)

#     class Meta:
#         unique_together = ('user','comment','time')



class Followers(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE ,related_name = "follow_user")
    follower = models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user','follower')

