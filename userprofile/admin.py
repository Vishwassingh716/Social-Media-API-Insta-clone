from django.contrib import admin

# Register your models here.

from .models import Posts,ProfilePage,LikePost,CommentOnPost

admin.site.register(ProfilePage)
admin.site.register(Posts)
admin.site.register(LikePost)
admin.site.register(CommentOnPost)

