from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.urls import reverse_lazy
from . models import Post
from .forms import PostingForm, RegistrationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, DeleteView

# Create your views here.
def index(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect("homepage")
        else:
            messages.info(request, "Invalid username or password.")
            return redirect("/")
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            confirm_password = form.cleaned_data.get("confirm_password")
        else:
            form = RegistrationForm()
            return render(request, 'register.html', {'form': form})

        if password == confirm_password:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Already Existed.")
                return redirect("register")
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username Already Existed.")
                return redirect("register")
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Account successfully created.")
            return redirect("/")
        else:
            messages.info(request, "Passwords do not match.")
            return redirect("register")
    form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

@login_required(login_url="/")
def homepage(request):
    if request.method == "POST":
        form = PostingForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
    form = PostingForm()
    posts = Post.objects.filter(user=request.user)
    content = {
        "form": form,
        "posts": posts
    }
    return render(request, "homepage.html", content)

def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user)
    content = {
        "username": username,
        "posts": posts
    }
    return render(request, "profile.html", content)

def post(request, username, id):
    post = Post.objects.get(id=id)
    content = {
        "username": username,
        "post": post
    }
    return render(request, "post.html", content)

def blogs(request):
    usernames = User.objects.values_list('username', flat=True)
    return render(request, "blogs.html", {'usernames': usernames})

def logout(request):
    auth.logout(request)
    messages.info(request, "You are logged out.")
    return redirect("/")

class UpdatePostView(UpdateView):
    model = Post
    template_name = 'edit.html'
    #fields = ['title', 'body']
    form_class = PostingForm

    def get_success_url(self) -> str:
        return reverse_lazy('homepage')

class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete.html'
    def get_success_url(self) -> str:
        return reverse_lazy('homepage')