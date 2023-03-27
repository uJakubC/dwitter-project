from django.urls import path

from .class_views import TweetListView, TweetDetailView

urlpatterns = [
    path("", TweetListView.as_view(), name="tweet-list"),
    path("dweet/<int:pk>", TweetDetailView.as_view(), name="tweet-detail")
    ]