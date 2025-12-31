from django import forms

from flux.models import Ticket


class TicketForm(forms.ModelForm):
    """ Form for creating ticket """
    class Meta:
        model = Ticket
        fields = ('ticket', 'description', 'image')
