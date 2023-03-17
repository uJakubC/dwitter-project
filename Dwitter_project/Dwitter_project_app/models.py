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
        return f"{self.body}"

    @property
    def o_username(self):
        return self.owner.username


class Likes(models.Model):
    owner = models.ForeignKey(USER, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Like Owner: {self.owner} | Tweet: {self.tweet} | Created at: {self.created_at}"


class Comments(models.Model):
    owner = models.ForeignKey(USER, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    body = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment Owner: {self.owner} | Tweet: {self.tweet} | Created at: {self.created_at}"
