from django.test import TestCase
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()


class TweetTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            username="test123",
            email="test@test.pl",
            password="secret_password"
        )

        cls.user2 = User.objects.create(
            username="user2",
            email="test@test.pl",
            password="secret_password"
        )

    def setUp(self):
        Tweet.objects.create(owner=self.user, body='Test body only testcase purposes')
        Tweet.objects.create(owner=self.user2, body='Test body for user2 only testcase purposes')

    def test_tweet_for_user1(self):
        tweet = Tweet.objects.get(owner=1)
        self.assertEqual(tweet.body, 'Test body only testcase purposes')
        self.assertEqual(tweet.o_username, 'test123')

    def test_tweet_o_username_for_user2(self):
        tweet = Tweet.objects.get(owner=2)
        self.assertEqual(tweet.o_username, 'user2')


class LikesTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            username="test123",
            email="test@test.pl",
            password="secret_password"
        )

    def setUp(self):
        self.tweet = Tweet.objects.create(owner=self.user, body='Test body only testcase purposes')
        self.like = Likes.objects.create(owner=self.user, tweet=self.tweet)

    def test_like_id(self):
        like = Likes.objects.get(id=1)
        self.assertEqual(like.id, 1)

    def test_like_owner(self):
        like = Likes.objects.get(id=1)
        self.assertEqual(like.o_username, "test123")
