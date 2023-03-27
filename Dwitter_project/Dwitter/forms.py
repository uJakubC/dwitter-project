from django import forms
from .models import Tweet, Likes, Comments


class AddTweetForm(forms.ModelForm):
    body = forms.CharField(
    widget=forms.widgets.Textarea(
        attrs={
            "placeholder": "Dweet something...",
            "rows": "4",
        }
    ),
    label = "",
    )

    class Meta:
        model = Tweet
        exclude = ('owner', 'created_at', 'updated_at')


class AddLikeForm(forms.ModelForm):
    class Meta:
        model = Likes
        exclude = ('owner', 'tweet', 'created_at', 'updated_at')


class AddCommentForm(forms.ModelForm):
    body = forms.CharField(
    widget=forms.widgets.Textarea(
        attrs={
            "placeholder": "Add your comment...",
            "rows": "3",
        }
    ),
    label="Comment",
    )

    class Meta:
        model = Comments
        exclude = ('owner', 'tweet', 'created_at', 'updated_at')
