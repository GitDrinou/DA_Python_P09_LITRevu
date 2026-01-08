import os
from typing import Iterable

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Model
from itertools import chain

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from litrevu import settings
from .forms import TicketForm, ReviewForm
from .models import Review, Ticket, UserFollows

User = get_user_model()


@login_required
def flux_page(request):
    """ Renders the home page for the connected user with his posts and
    followed users posts """
    followed_users = UserFollows.objects.filter(
        user=request.user
    ).values_list('followed_user', flat=True)
    users = list(followed_users)
    users.append(request.user.id)
    tickets: Iterable[Ticket] = Ticket.objects.filter(user__in=users)
    reviews: Iterable[Review] = Review.objects.filter(user__in=users)

    connected_user_tickets = Ticket.objects.filter(user=request.user)
    reviews_on_user_tickets = Review.objects.filter(
        ticket_id__in=connected_user_tickets
    )

    all_reviews = reviews.union(reviews_on_user_tickets)

    flux = sorted(
        chain(tickets, all_reviews),
        key=lambda obj: obj.time_created,
        reverse=True
    )
    user_reviewed_tickets = Review.objects.filter(
        user=request.user).values_list(
        'ticket_id', flat=True).distinct()

    return render(
        request,
        'flux/flux.html',
        context={
            'flux': flux,
            'user_reviewed_tickets': user_reviewed_tickets
        }
    )


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
        if ticket.image:
            image_path = os.path.join(settings.MEDIA_ROOT, str(ticket.image))
            if os.path.exists(image_path):
                os.remove(image_path)

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
def add_review_to_ticket(request, ticket_id):
    """ Adds a review for a ticket
        Args:
            request: HttpRequest
            ticket_id: id of the ticket to be reviewed.
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES, prefix="review")
        if form.is_valid():
            with transaction.atomic():
                review = form.save(commit=False)
                review.user = request.user
                review.ticket = ticket
                review.save()
            return redirect('home')
    else:
        form = ReviewForm(prefix="review")

    return render(request, 'flux/review_form.html', context={
            "ticket": ticket,
            "form": form,
        })


@login_required
def subscriptions_page(request):
    """ Returns the subscriptions page
        Args:
            request: HttpRequest
    """
    current_user = request.user
    search_query = request.GET.get('search', '')

    if request.method == 'GET' and search_query:
        try:
            followed_user = User.objects.get(username__iexact=search_query)
            if followed_user != current_user:
                if not UserFollows.objects.filter(
                        user=current_user,
                        followed_user=followed_user
                ).exists():
                    UserFollows.objects.create(
                        user=current_user,
                        followed_user=followed_user
                    )
                else:
                    messages.info(
                        request,
                        f"Vous suivez déjà {followed_user.username}")
            else:
                messages.warning(
                    request,
                    "Vous ne pouvez pas vous abonnez vous-même.")
        except User.DoesNotExist:
            messages.warning(
                request,
                f"L'utilisateur {search_query} n'existe pas.")

    following = UserFollows.objects.filter(
        user=current_user
    ).select_related('followed_user')

    followers = UserFollows.objects.filter(
        followed_user=current_user
    ).select_related('user')

    context = {
        'following': following,
        'followers': followers,
        'search_query': search_query,
    }

    return render(request, 'flux/subscriptions.html', context)


@login_required
def unfollow_user(request, user_id):
    """ Unfollows a user
        Args:
            request: HttpRequest
            user_id: id of the user to be unfollowed
    """
    followed_user = get_object_or_404(User, id=user_id)
    UserFollows.objects.filter(user=request.user,
                               followed_user=followed_user).delete()
    return redirect('subscriptions')
