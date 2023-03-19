from django.db import IntegrityError
from django.db.models import Count
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.generic import View

from .forms import AddTweetForm
from .models import Tweet, Likes


class TweetListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        tweets = Tweet.objects.all()
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

            tweets = Tweet.objects.all()    # Load all tweets once again
            likes = Likes.objects.values('tweet_id').annotate(total=Count('tweet_id'))
            form = AddTweetForm()   # Load clean form
            context = {'tweets': tweets, 'likes': likes, 'form': form}
        else:
            tweets = Tweet.objects.all()  # Load all tweets once again
            likes = Likes.objects.values('tweet_id').annotate(total=Count('tweet_id'))
            form = AddTweetForm()  # Load clean form
            context = {'tweets': tweets, 'likes': likes, 'form': form}

        return render(request=request, template_name='tweet_list.html', context=context)


class TweetDetailView(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        try:
            tweet = Tweet.objects.get(pk=pk)
            likes = Likes.objects.filter(tweet_id=pk).count()
            context = {'tweet': tweet, 'likes': likes}

            return render(request=request, template_name="tweet_detail.html", context=context)
        except Tweet.DoesNotExist:
            return HttpResponseNotFound("<h1>Page does not exist</h1> <img src='https://as2.ftcdn.net/v2/jpg/03/39/94/53/1000_F_339945393_2xeDV1SAYvwQTrEQXtuO7lUfpJEOzOVr.jpg' >")
