from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import DetailView, UpdateView, DeleteView
from .form import UserForm
from .mixins import OnlyYouMixin
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


def index(request):
    return render(request, "app/index.html")

def home(request):
    return render(request, "app/home.html")

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user_instance = form.save()
            login(request, user_instance)
            return redirect("app:home")
    else:
        form = UserCreationForm()

    context = {
        "form": form
    }
    return render(request, 'app/signup.html',context)

@login_required
def home(request):
    return render(request, "app/home.html")

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "app/users/detail.html"
    form_class = UserForm

    def get_success_url(self):
        return resolve_url('app:users_detail', pk=self.kwargs['pk'])

class UserUpdateView(OnlyYouMixin, UpdateView):
    model = User
    template_name = "app/users/update.html"
    form_class = UserForm

    def get_success_url(self):
        return resolve_url('app:users_detail', pk=self.kwargs['pk'])

class UserDeleteView(OnlyYouMixin, DeleteView):
    model = User
    template_name = "app/users/delete.html"

    def get_success_url(self):
        return resolve_url('app:users_detail', pk=self.kwargs['pk'])
