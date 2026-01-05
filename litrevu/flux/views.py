from typing import Iterable

from django.db import transaction
from django.db.models import Model
from itertools import chain

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .forms import TicketForm, ReviewForm
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
        ticket = get_object_or_404(
            Ticket,
            id=ticket_id,
            user=request.user
        )
        form = TicketForm(
            request.POST or None,
            request.FILES or None,
            instance=ticket
        )
    else:
        form = TicketForm(request.POST or None, request.FILES or None)

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
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    if request.method == 'POST':
        ticket.delete()
        return redirect('home')

    context = {
        "object_type": "le ticket",
        "object_label": ticket.ticket,
        "cancel_url": reverse('posts'),
    }
    return render(request, 'flux/deleted_confirm.html', context=context)


@login_required
def add_ticket_with_review(request):
    """ Adds or updates a review
        Args:
            request: HttpRequest
    """

    ticket_form = TicketForm(prefix="ticket")
    review_form = ReviewForm(prefix="review")

    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES, prefix="ticket")
        review_form = ReviewForm(request.POST, prefix="review")

        if ticket_form.is_valid() and review_form.is_valid():
            with transaction.atomic():
                ticket = ticket_form.save(commit=False)
                ticket.user = request.user
                ticket.save()

                review = review_form.save(commit=False)
                review.user = request.user
                review.ticket = ticket
                review.save()
            return redirect('home')

    return render(
        request,
        'flux/ticket_review_form.html',
        context={
            "ticket_form": ticket_form,
            "review_form": review_form,
        }
    )


@login_required
def update_review(request, review_id):
    """ Adds or updates a review
        Args:
            request: HttpRequest
            review_id: id of the review to be updated. By default: None
    """

    review = get_object_or_404(
        Review.objects.select_related("ticket"),
        pk=review_id,
        user=request.user
    )
    ticket = review.ticket

    if request.method == 'POST':
        form = ReviewForm(request.POST or None, request.FILES or None,
                          instance=review)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ReviewForm(instance=review)

    return render(
        request,
        'flux/review_form.html',
        context={'form': form, 'ticket': ticket}
    )


@login_required
def delete_review(request, review_id):
    """ Deletes a review
        Args:
            request: HttpRequest
            review_id: id of the ticket to be deleted
    """
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        review.delete()
        return redirect('home')

    context = {
        "object_type": "la critique",
        "object_label": review.headline,
        "cancel_url": reverse('posts'),
    }
    return render(request, 'flux/deleted_confirm.html', context=context)


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
    return render(request, 'flux/posts.html', context={'posts': posts})
