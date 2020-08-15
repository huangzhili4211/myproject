from django import forms
from .models import Topic, Board, Usermodel, Blog


class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(),
        max_length=4000000,
        help_text='The max length of the text is 4000000.'
    )

    class Meta:
        model = Topic
        fields = ['subject', 'message']


class NewBlogForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(),
        max_length=30,
        help_text='The max length of the text is 4000.'
    )

    class Meta:
        model = Blog 
        fields = ['subject', 'message']

class Userform(forms.ModelForm):

    username = forms.CharField(
        help_text='please input your username.'

    )

    password = forms.CharField(
        help_text='please input your password.'

    )

    class Meta:
        model = Usermodel
        fields = ['username','password']
