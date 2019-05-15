from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
# Create your views here.
from user.forms import AddUserForm, LoginForm


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
            email = form.cleaned_data['email']
            if query.exists():
                return render(request, 'add_user.html', {'form':form, 'message': 'This username already exists'})
            else:
                user = User.objects.create_user(\
                    username=username, password=password, email=email)
                #return render(request, 'add_user.html', {'form':AddUserForm(), 'message':'Done'})
                return redirect('/play')
        else:
            return render(request, 'add_user.html', {'form':form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form':form})
    def post(self, request):
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
               return render(request, 'add_user.html', {'form': form, 'message': 'There is no such a user'})
        else:
            return render(request, 'login.html', {'form':form})
