from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404

from accounts.forms import PostForm
from .forms import NewTopicForm, Userform
from .models import Board, Topic, Post, Usermodel


# Create your views here.



def home(request):
    boards = Board.objects.all()
    return render(request,'home.html',{'boards':boards})

def board_topics(request,pk):
    board = get_object_or_404(Board,pk=pk)
    return render(request,'topics.html',{'board':board})

@login_required
def new_topic(request,pk):
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request,'new_topic.html',{'board':board,'form':form})


def form(request):
    if request.method == 'POST':
        form = Userform(request.POST)
        if form.is_valid():
            new_user = Usermodel.objects.create(
                username = form.cleaned_data.get('username'),
                password = form.cleaned_data.get('password')

            )
    else:
        form = Userform()
    return render(request,'userform.html',{'form':form})

def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic,board_id=pk,pk=topic_pk)
    topic.views+=1
    topic.save()
    return render(request,'topic_posts.html',{'topic':topic})


@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})

def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    return render(request, 'topics.html', {'board': board, 'topics': topics})

def test(request):
    return render(request, 'test.html')