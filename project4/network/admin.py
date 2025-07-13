from django.contrib import admin
from .models import Posts,User,Follow,Like
# Register your models here.


admin.site.register(Posts)
admin.site.register(User)
admin.site.register(Follow)
admin.site.register(Like)