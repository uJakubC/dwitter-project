from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.generic import View

from .models import Tweet


class TweetListView(View):
    def get(self, request:HttpRequest) -> HttpResponse:
        tweets = Tweet.objects.all().values()
        context = {'tweets': tweets}

        return render(request=request, template_name="tweet_list.html", context=context)
