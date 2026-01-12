from django.contrib.auth import get_user_model
from django.test import TestCase

from flux.models import Ticket, Review, UserFollows

User = get_user_model()


class TestTicketModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="pass321",
        )
        self.ticket = Ticket.objects.create(
            ticket="Ticket Test 1",
            description="Description Ticket Test 1",
            user=self.user,
        )

    def test_ticket_creation(self):
        self.assertEqual(self.ticket.ticket, "Ticket Test 1")
        self.assertEqual(self.ticket.description, "Description Ticket Test 1")
        self.assertEqual(self.ticket.user, self.user)
        self.assertIsNotNone(self.ticket.time_created)


class TestReviewModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="pass321",
        )
        self.ticket = Ticket.objects.create(
            ticket="Ticket Test 1",
            user=self.user,
        )
        self.review = Review.objects.create(
            ticket=self.ticket,
            rating=3,
            user=self.user,
            headline="Review Ticket Test 1",
            body="Body Review Ticket Test 1",
        )

    def test_review_creation(self):
        self.assertEqual(self.review.ticket, self.ticket)
        self.assertEqual(self.review.rating, 3)
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.review.headline, "Review Ticket Test 1")
        self.assertEqual(self.review.body, "Body Review Ticket Test 1")
        self.assertIsNotNone(self.review.time_created)


class TestUserFollowModel(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testuser1",
            password="pass321",
        )
        self.user2 = User.objects.create_user(
            username="testuser2",
            password="pass987",
        )

    def test_user_following_creation(self):
        follow = UserFollows.objects.create(
            user=self.user1,
            followed_user=self.user2,
        )
        self.assertEqual(follow.user, self.user1)
        self.assertEqual(follow.followed_user, self.user2)
