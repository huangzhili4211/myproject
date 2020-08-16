from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404

from accounts.forms import PostForm
from .forms import NewTopicForm, Userform, NewBlogForm
from .models import Board, Topic, Post, Usermodel, Blog
from django.views.generic import UpdateView, ListView
from django.utils import timezone
from django.utils.decorators import method_decorator

# Create your views here.


'''
def home(request):
    boards = Board.objects.all()
    return render(request,'home.html',{'boards':boards})

def board_topics(request,pk):
    board = get_object_or_404(Board,pk=pk)
    return render(request,'topics.html',{'board':board})
'''
class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 20
    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)
    
    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset


class BoardListView(ListView):
	model = Board
	context_object_name = 'boards'
	template_name = 'home.html'



@login_required
def createblog(request):
    user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        form = NewBlogForm(request.POST)
        boards = Board.objects.all()
        if form.is_valid():
            blog = form.save(commit=False)
            blog.starter = request.user
            blog.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=blog,
                created_by=request.user
            )
            return redirect('bloglist')  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request,'new_blog.html',{'form':form})
    
def bloglist(request):
    blogs = Blog.objects.all 
    return render(request, 'blog_list.html')
    

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

@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
	model = Post
	fields = ('message', )
	template_name = 'edit_post.html'
	pk_url_kwarg = 'post_pk'
	context_object_name = 'post'
		
	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(created_by=self.request.user)

	def form_valid(self, form):
		post = form.save(commit=False)
		post.updated_by = self.request.user
		post.updated_at = timezone.now()
		post.save()
		return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)



class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 2
    
    def get_context_data(self, **kwargs):
        self.topic.views += 1
        self.topic.save()
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset

