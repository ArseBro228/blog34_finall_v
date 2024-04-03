from django import forms

from .models import Post, Tag, Photo


class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    image = forms.ModelMultipleChoiceField(
        queryset=Photo.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Post
        exclude = ('published_date', 'comments', 'user')


