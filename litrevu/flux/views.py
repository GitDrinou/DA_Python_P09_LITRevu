from typing import Iterable
from django.db.models import Model
from itertools import chain

from . import forms
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Review, Ticket


@login_required
def flux_page(request):
    """ Renders the home page for connected users """
    tickets: Iterable[Model] = Ticket.objects.all()
    reviews: Iterable[Model] = Review.objects.all()
    flux = sorted(
        chain(tickets, reviews),
        key=lambda obj: obj.time_created,
        reverse=True
    )
    return render(request, 'flux/flux.html', {'flux': flux})


@login_required
def ticket_page(request):
    """ Adds a new ticket """
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')
        else:
            form = forms.TicketForm()
    return render(
        request,
        'flux/ticket_form.html',
        context={'form': form}
    )
