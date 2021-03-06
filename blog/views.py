from django.contrib.auth import login
from django.shortcuts import render, get_object_or_404

from blog.forms import CreateCommentForm, NewUserForm
from blog.models import Topic, Post, Comment
from django.views.generic import CreateView, DetailView
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from .forms import CreateCommentForm

from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm


def get_topics(request):
    topics = Topic.objects.all()
    context = {
        "topics": topics
    }
    return render(request, "topics.html", context)


def get_topic_posts(requests, pk):
    posts = Post.objects.filter(topic__id=pk)
    context = {
        'posts': posts,
        'topic_id': pk,
    }
    return render(requests, "posts.html", context)


def like_view(request, pk):
    id = request.POST.get("post_id")
    post = Post.objects.get(id=id)
    post.likes_count += 1
    post.save()
    return HttpResponseRedirect(reverse("posts", args=[str(pk)]))


class AddTopicView(CreateView):
    model = Topic
    template_name = "create_topic.html"
    fields = '__all__'


class AddPostView(CreateView):
    model = Post
    template_name = "add_post.html"
    fields = 'topic', 'text', 'name'


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'


class CreateCommentView(CreateView):
    model = Comment
    template_name = 'create_comment.html'
    fields = 'post', 'text', 'rating'
    # form_class = CreateCommentForm


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("topics")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("topics")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("topics")
