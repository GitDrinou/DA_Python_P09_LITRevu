"""
URL configuration for litrevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path

import authentication.views
import flux.views
from litrevu.constants import PAGES_NAME, PAGES_URL

urlpatterns = [
    path(PAGES_URL['u_admin'], admin.site.urls),
    path(PAGES_URL['u_login'], LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True,
    ), name=PAGES_NAME['p_login']),
    path(PAGES_URL['u_logout'], authentication.views.logout_user,
         name=PAGES_NAME['p_logout']),
    path(PAGES_URL['u_home'], flux.views.home, name=PAGES_NAME['p_home']),
    path(PAGES_URL['u_signup'], authentication.views.signup_page,
         name=PAGES_NAME['p_signup']),
]
