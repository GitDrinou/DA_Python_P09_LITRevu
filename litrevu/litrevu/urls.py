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
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path

import authentication.views
import flux.views
from litrevu import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True,
    ), name='login'),
    path('logout/', authentication.views.logout_user, name='logout'),
    path('home/', flux.views.flux_page, name='home'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('ticket/', flux.views.add_or_update_ticket, name='ticket_create'),
    path('ticket/<int:ticket_id>/edit/', flux.views.add_or_update_ticket,
         name='ticket_edit'),
    path('ticket/<int:ticket_id>/delete/', flux.views.delete_ticket,
         name='ticket_delete'),
    path('review/', flux.views.add_or_update_review, name='review_create'),
    path('posts/', flux.views.get_posts, name='posts'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
