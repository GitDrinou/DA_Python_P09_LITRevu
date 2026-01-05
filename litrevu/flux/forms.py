from django import forms

from flux.models import Ticket, Review


class TicketForm(forms.ModelForm):
    """ Form for ticket """
    class Meta:
        model = Ticket
        fields = ('ticket', 'description', 'image')
        labels = {
            "ticket": "Titre",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 10}),
        }


class ReviewForm(forms.ModelForm):
    """ Form for ticket """
    class Meta:
        RATING_CHOICES = [
            (0, "0"),
            (1, "1"),
            (2, "2"),
            (3, "3"),
            (4, "4"),
            (5, "5"),
        ]
        model = Review
        fields = ('rating', 'headline', 'body')
        labels = {
            "rating": "Note",
            "headline": "Titre",
            "body": "Commentaire",
        }
        widgets = {
            "rating": forms.RadioSelect(choices=RATING_CHOICES),
            "body": forms.Textarea(attrs={"rows": 12}),
        }
