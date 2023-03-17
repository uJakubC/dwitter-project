from django.db import IntegrityError
from django.db.models import Count
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.views.generic import View

from .forms import AddTweetForm
from .models import Tweet, Likes


class TweetListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        tweets = Tweet.objects.all().values()
        likes = Likes.objects.values('tweet_id').annotate(total=Count('tweet_id'))
        form = AddTweetForm()
        
        if tweets:
            context = {'tweets': tweets, 'likes': likes, 'form': form}
            return render(request=request, template_name="tweet_list.html", context=context)
        else:
            context = {'tweets': tweets, 'empty_query': True, 'form': form}
            return render(request=request, template_name="tweet_list.html", context=context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = AddTweetForm(request.POST)
        if form.is_valid():
            try:
                tweet = form.save(commit=False)
                tweet.owner = request.user
                tweet.save()
            except IntegrityError:
                return HttpResponseBadRequest("Bad request")

            tweets = Tweet.objects.all().values() # Load all tweets once again
            likes = Likes.objects.values('tweet_id').annotate(total=Count('tweet_id'))
            form = AddTweetForm() # Load clean form
            context = {'tweets': tweets, 'likes': likes, 'form': form}
        else:
            tweets = Tweet.objects.all().values()  # Load all tweets once again
            likes = Likes.objects.values('tweet_id').annotate(total=Count('tweet_id'))
            form = AddTweetForm()  # Load clean form
            context = {'tweets': tweets, 'likes': likes, 'form': form}

        return render(request=request, template_name='tweet_list.html', context=context)
