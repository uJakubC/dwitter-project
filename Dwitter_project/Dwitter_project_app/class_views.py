from django.db import IntegrityError
from django.db.models import Count
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.generic import View

from .forms import AddTweetForm, AddLikeForm, AddCommentForm
from .models import Tweet, Likes, Comments


class TweetListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        tweets = Tweet.objects.all()
        likes = Likes.objects.values('tweet_id').annotate(total=Count('tweet_id'))
        comments = Comments.objects.values('tweet_id').annotate(total=Count('tweet_id'))
        last_five_tweets = tweets.order_by('id')[:5]
        form = AddTweetForm()

        if tweets:
            context = {'tweets': tweets, 'likes': likes, 'form': form, 'comments': comments, 'last_five_tweets': last_five_tweets}
            return render(request=request, template_name="tweet_list.html", context=context)
        else:
            context = {'tweets': tweets, 'empty_query': True, 'form': form, 'comments': comments, 'last_five_tweets': last_five_tweets}
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
        comments = Comments.objects.values('tweet_id').annotate(total=Count('tweet_id'))
        form = AddTweetForm()   # Load clean form
        context = {'tweets': tweets, 'likes': likes, 'form': form, 'comments': comments, 'last_five_tweets': last_five_tweets}

        return render(request=request, template_name='tweet_list.html', context=context)


class TweetDetailView(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        like_form = AddLikeForm()
        comment_form = AddCommentForm()
        try:
            tweet = Tweet.objects.get(pk=pk)
            likes = Likes.objects.filter(tweet_id=pk).count()
            comments = Comments.objects.filter(tweet_id=pk)
            context = {
                'tweet': tweet,
                'likes': likes,
                'comments': comments,
                'like_form': like_form,
                'comment_form': comment_form
            }

            return render(request=request, template_name="tweet_detail.html", context=context)
        except Tweet.DoesNotExist:
            return HttpResponseNotFound("<h1>Page does not exist</h1> <img src='https://as2.ftcdn.net/v2/jpg/03/39/94/53/1000_F_339945393_2xeDV1SAYvwQTrEQXtuO7lUfpJEOzOVr.jpg' >")

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        tweet = Tweet.objects.get(pk=pk)
        like_form = AddLikeForm(request.POST)
        comment_form = AddCommentForm(request.POST)

        if 'like_button' in request.POST:
            if like_form.is_valid():
                try:
                    like = like_form.save(commit=False)
                    like.owner = request.user
                    like.tweet = tweet
                    like.save()
                except IntegrityError:
                    return HttpResponseBadRequest("Bad request")

        elif 'comment_button' in request.POST:
            if comment_form.is_valid():
                try:
                    comment = comment_form.save(commit=False)
                    comment.owner = request.user
                    comment.tweet = tweet
                    comment.save()
                except IntegrityError:
                    return HttpResponseBadRequest("Bad request")

        likes = Likes.objects.filter(tweet_id=pk).count()
        comments = Comments.objects.filter(tweet_id=pk)
        comment_form = AddCommentForm()
        context = {
            'tweet': tweet,
            'likes': likes,
            'comments': comments,
            'like_form': like_form,
            'comment_form': comment_form
        }

        return render(request=request, template_name="tweet_detail.html", context=context)