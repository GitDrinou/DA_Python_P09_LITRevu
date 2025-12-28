from django.contrib.auth import logout, login
from django.shortcuts import redirect, render

from authentication.forms import SignUpForm
from litrevu import settings
from . import forms


def logout_user(request):
    """ Renders the logout process """
    logout(request)
    return redirect('login')

def signup_page(request):
    """ Renders the signup process """
    form = SignUpForm()
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(
        request,
        'authentication/signup.html',
        context={'form': form}
    )
