from django.urls import path

from .class_views import TweetListView

urlpatterns = [
    path("", TweetListView.as_view(), name="tweet-list"),
    ]