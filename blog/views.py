import datetime
import logging

logger = logging.getLogger(__name__)

from django.views import generic
from .models import Post
from rest_framework import viewsets
from .serializers import PostSerializer

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUserForm

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        logger.warning('Homepage was accessed at ' + str(datetime.datetime.now()) + ' hours!')
        return super().get(request, *args, **kwargs)

class PostDetail(generic.DetailView):
    model = Post
    template_name = 'post_detail.html'

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


def register_request(request):
    if request.method == "POST":
        register_form = NewUserForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("home")
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        register_form = NewUserForm()
    return render(request=request, template_name="blog/register.html", context={"register_form": register_form})
def login_request(request):
    if request.method == "POST":
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        login_form = AuthenticationForm()
    return render(request=request, template_name="blog/login.html", context={"login_form": login_form})
def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("home")