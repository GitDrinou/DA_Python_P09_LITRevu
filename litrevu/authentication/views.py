from django.contrib.auth import logout
from django.shortcuts import redirect


def logout_user(request):
    """ Renders the logout process """
    logout(request)
    return redirect('login')