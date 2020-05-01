from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView, ListView
from .form import UserForm, ListForm, CardForm, CardCreateFromHomeForm
from .mixins import OnlyYouMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import List, Card
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

class HomeView(LoginRequiredMixin, ListView):
    model = List
    template_name = "app/home.html"

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

class ListCreateView(LoginRequiredMixin, CreateView):
    model = List
    template_name = "app/Lists/create.html"
    form_class = ListForm
    success_url = reverse_lazy("app:home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ListListView(LoginRequiredMixin, ListView):
    model = List
    template_name = "app/lists/list.html"

class ListDetailView(LoginRequiredMixin, DetailView):
    model = List
    template_name = "app/lists/detail.html"

class ListUpdateView(LoginRequiredMixin, UpdateView):
    model = List
    template_name = "app/lists/update.html"
    form_class = ListForm
    success_url = reverse_lazy("app:home")

class ListDeleteView(LoginRequiredMixin, DeleteView):
    model = List
    template_name = "app/lists/delete.html"
    form_class = ListForm
    success_url = reverse_lazy("app:home")

class CardCreateView(LoginRequiredMixin, CreateView):
    model = Card
    template_name = "app/cards/create.html"
    form_class = CardForm
    success_url = reverse_lazy("app:home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CardListView(LoginRequiredMixin, ListView):
    model = Card
    template_name = "app/cards/list.html"

class CardDetailView(LoginRequiredMixin, DetailView):
    model = Card
    template_name = "app/cards/detail.html"

class CardUpdateView(LoginRequiredMixin, UpdateView):
    model = Card
    template_name = "app/cards/update.html"
    form_class = CardForm
    success_url = reverse_lazy("app:home")

class CardDeleteView(LoginRequiredMixin, DeleteView):
    model = Card
    template_name = "app/cards/delete.html"
    form_class = CardForm
    success_url = reverse_lazy("app:home")

class CardCreateFromHomeView(LoginRequiredMixin, CreateView):
    model = Card
    template_name = 'app/cards/create.html'
    form_class = CardCreateFromHomeForm
    success_url = reverse_lazy("app:home")

    def form_valid(self, form):
        list_pk = self.kwargs['list_pk']
        list_instance = get_object_or_404(List, pk=list_pk)
        form.instance.list = list_instance
        form.instance.user = self.request.user
        return super().form_valid(form)
