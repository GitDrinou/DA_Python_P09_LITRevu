from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from flux.models import UserFollows, Ticket, Review

User = get_user_model()


class TestFluxPageView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1',
                                              password='pass321')
        self.user2 = User.objects.create_user(username='user2',
                                              password='pass987')
        self.user3 = User.objects.create_user(username='user3',
                                              password='pass654')
        self.user1_follows_user2 = UserFollows.objects.create(
            user=self.user1, followed_user=self.user2)
        self.ticket1 = Ticket.objects.create(
            ticket='Ticket 1',
            description='description1',
            user=self.user1,
            image='image1.png',
        )
        self.ticket2 = Ticket.objects.create(
            ticket='Ticket 2',
            description='description2',
            user=self.user2,
        )
        self.review1 = Review.objects.create(
            ticket=self.ticket1,
            rating=2,
            user=self.user1,
            headline='Review 1',
        )
        self.client.login(username='user1', password='pass321')

    def test_flux_page_contains_user_and_followed(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'flux/flux.html')
        self.assertContains(response, "Ticket 1")
        self.assertContains(response, "Ticket 2")
        self.assertContains(response, "Review 1")

    def test_flux_page_not_contains_unfollowed_ticket(self):
        Ticket.objects.create(
            ticket='Ticket 3',
            user=self.user3,
        )
        response = self.client.get(reverse('home'))
        self.assertNotContains(response, 'Ticket 3')


class TestAddOrUpdateTicketView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user1',
                                             password='pass321')
        self.client.login(username='user1', password='pass321')

    def test_add_ticket(self):
        response = self.client.post(
            reverse('ticket_create'),
            data={
                'ticket': 'Ticket 1',
                'description': 'description1',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Ticket.objects.count(), 1)

    def test_update_ticket(self):
        ticket = Ticket.objects.create(ticket='Ancien Ticket 1',
                                       user=self.user,)
        response = self.client.post(
            reverse('ticket_edit', args=[ticket.id]),
            data={
                'ticket': 'Ticket 1 Mis à jour',
                'description': 'nouvelle description 1',
            }
        )
        self.assertEqual(response.status_code, 302)
        ticket.refresh_from_db()
        self.assertEqual(ticket.ticket, 'Ticket 1 Mis à jour')


class TestDeleteTicketView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user1',
                                             password='pass321')
        self.client.login(username='user1', password='pass321')
        self.ticket = Ticket.objects.create(
            ticket='Ticket A Supprimer',
            user=self.user,
        )

    def test_delete_ticket(self):
        response = self.client.post(
            reverse('ticket_delete', args=[self.ticket.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Ticket.objects.count(), 0)


class TestAddTicketWithReviewView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user1',
                                             password='pass321')
        self.client.login(username='user1', password='pass321')

    def test_add_ticket_with_review(self):
        response = self.client.post(
            reverse('review_create'),
            data={
                'ticket-ticket': 'Ticket 1',
                'ticket-description': 'description1',
                'ticket-image': 'image1.png',
                'review-rating': 2,
                'review-headline': 'Review 1',
                'review-body': 'Review body',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Ticket.objects.count(), 1)
        self.assertEqual(Review.objects.count(), 1)


class TestSubscriptionView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='user1',
            password='pass321'
        )
        self.user2 = User.objects.create_user(username='user2',
                                              password='pass987')
        self.client.login(username='user1', password='pass321')

    def test_follow_user(self):
        response = self.client.get(
            reverse('subscriptions'), {'search': 'user2'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(UserFollows.objects.filter(
            user=self.user1,
            followed_user=self.user2,
        ).exists())

    def test_unfollow_user(self):
        UserFollows.objects.create(user=self.user1, followed_user=self.user2)
        response = self.client.post(reverse('unfollow_user',
                                            args=[self.user2.id]),)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(UserFollows.objects.filter(
            user=self.user1,
            followed_user=self.user2,
        ).exists())
