from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from boards.models import Post

class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ['username', 'email','password1', 'password2']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message',]
