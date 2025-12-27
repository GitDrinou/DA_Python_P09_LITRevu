from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from . import forms

def login_page(request):
    """ Renders the login page """
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                message = 'Identifiants invalides'
    return render(
        request,
        'authentication/login.html',
        context={'form':form, 'message': message}
    )

def logout_user(request):
    """ Renders the logout process """
    logout(request)
    return redirect('login')