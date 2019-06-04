from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
# Create your views here.
from django.views.generic import FormView
from user.forms import AddUserForm, LoginForm, LogoutForm


class AddUserView(View):
    def get(self, request):
        form = AddUserForm()
        return render(request, 'add_user.html', {'form':form})
    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            query = User.objects.filter(username=username)
            password = form.cleaned_data['password']
            if query.exists():
                return render(request, 'add_user.html', {'form':form, 'message': 'This username already exists'})
            else:
                user = User.objects.create_user(
                    username=username, password=password)
                return redirect('/play')
        else:
            return render(request, 'add_user.html', {'form':form})


class LoginView(View):
    def get(self, request):
        print("GET")
        form = LoginForm()
        return render(request, 'login.html', {'form':form})
    def post(self, request):
        print("POST")
        form = LoginForm(request.POST)
        if form.is_valid():
           username = form.cleaned_data['username']
           password = form.cleaned_data['password']
           user = authenticate(username=username, password=password)
           if user is not None:
               if user.is_active:
                   login(request, user)
                   return redirect('/play')
           else:
               return HttpResponseRedirect('/add')
        else:
            return HttpResponseRedirect('/login')


class LogoutView(FormView):
    template_name = 'logout.html'
    form_class = LogoutForm
    success_url = '/login'
    def form_valid(self, form):
        logout(self.request)
        return super(LogoutView, self).form_valid(form)
