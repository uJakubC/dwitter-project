from django import forms
from .models import Tweet


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
