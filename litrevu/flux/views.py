from typing import Iterable
from django.db.models import Model
from itertools import chain

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from . import forms, models
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
def add_or_update_ticket(request, ticket_id=None):
    """ Adds or updates a ticket
        Args:
            request: HttpRequest
            ticket_id: id of the ticket to be updated. By default: None
    """
    if ticket_id:
        ticket = get_object_or_404(models.Ticket, id=ticket_id,
                                   user=request.user)
        form = forms.TicketForm(request.POST or None, request.FILES or None,
                                instance=ticket)
    else:
        form = forms.TicketForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')

    return render(
        request,
        'flux/ticket_form.html',
        context={'form': form}
    )


@login_required
def delete_ticket(request, ticket_id):
    """ Deletes a ticket
        Args:
            request: HttpRequest
            ticket_id: id of the ticket to be deleted
    """
    ticket = get_object_or_404(models.Ticket, id=ticket_id, user=request.user)
    if request.method == 'POST':
        ticket.delete()
        return redirect('home')
    return render(request, 'flux/deleted_confirm.html', context={
        'ticket': ticket})


@login_required
def get_posts(request):
    """ Returns a list of all tickets """
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()
    list_tickets: Iterable[Model] = tickets.filter(user=request.user)
    list_reviews: Iterable[Model] = reviews.filter(user=request.user)
    posts = sorted(
        chain(list_tickets, list_reviews),
        key=lambda obj: obj.time_created,
        reverse=True
    )
    return render(request, 'flux/tickets.html', context={'posts': posts})
