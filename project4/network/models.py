from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Posts(models.Model):
    content = models.CharField(max_length=164)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Post {self.id} by {self.user} on {self.date}"
    
class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_following")
    user_follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_being_followed")

    def __str__(self):
        return f"{self.user} is following {self.user_follower} "
    


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="like_user")
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="like_post")


    def __str__(self):
        return f"{self.user} liked the post {self.post}"