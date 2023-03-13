from django.conf import settings
from django.db import models

# Constant that states for user model to use for the Foreign Keys
USER = settings.AUTH_USER_MODEL


class Tweet(models.Model):
    owner = models.ForeignKey(USER, on_delete=models.CASCADE)
    body = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Owner: {self.owner}, body: {self.body}"


class Likes(models.Model):
    owner = models.ForeignKey(USER, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):
    owner = models.ForeignKey(USER, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    body = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
