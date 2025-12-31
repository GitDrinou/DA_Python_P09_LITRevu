from . import forms
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def flux_page(request):
    """ Renders the home page for connected users """
    return render(request, 'flux/flux.html')


@login_required
def ticket_page(request):
    """ Adds a new ticket """
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(
        request,
        'flux/ticket_form.html',
        context={'form': form}
    )
