
import datetime

from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question, Choice
import logging


def create_question(text, days):
    time=timezone.now()+datetime.timedelta(days=days)
    return(Question.objects.create(text=text, productiondate=time))
class QuestionModelTest(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(productiondate=time)
        self.assertIs(future_question.was_published_recently(), False)
class IndexViewTest(TestCase):
    def test_no_questions(self):
        response=self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(text="Past question.", days=-30)
        question.choice_set.create(choice_text="1", votes=0)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(text="Past question.", days=-30)
        question.choice_set.create(choice_text="1", votes=0)
        create_question(text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(text="Past question 1.", days=-30)
        question1.choice_set.create(choice_text="1", votes=0)
        question2 = create_question(text="Past question 2.", days=-5)
        question2.choice_set.create(choice_text="1", votes=0)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )
    def test_question_with_no_choices(self):
        q=create_question(text="no", days=-1)
        response=self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [])
    def test_question_with_choices(self):
        q=create_question(text="yes", days=-1)
        q.choice_set.create(choice_text="a", votes=0)
        response=self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"], [q],)
class DetailViewTest(TestCase):
    def test_future_question(self):
        q=create_question(text="Future", days=30)
        q.choice_set.create(choice_text="1", votes=0)
        response=self.client.get(reverse("polls:detail", args=(q.id,)))
        self.assertEqual(response.status_code, 404)
    def test_past_question(self):
        q=create_question(text="past", days=-30)
        q.choice_set.create(choice_text="1", votes=0)
        response=self.client.get(reverse("polls:detail", args=(q.id,)))
        self.assertContains(response, q.text)
class ResultsViewTest(TestCase):
    def test_future_question(self):
        q=create_question(text="Future", days=30)
        q.choice_set.create(choice_text="1", votes=0)
        response=self.client.get(reverse("polls:results", args=(q.id,)))
        self.assertEqual(response.status_code, 404)
    def test_past_question(self):
        q=create_question(text="Past", days=-30)
        q.choice_set.create(choice_text="1", votes=0)
        response=self.client.get(reverse("polls:results", args=(q.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, q.text)
class NullingViewTest(TestCase):
    def test_nulling(self):
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        test_user2.save()
        permission=Permission.objects.get(name="User can nullify votes")
        test_user2.user_permissions.add(permission)
        self.client.login(username='testuser2',password='2HJ1vRV0Z&3iD' )
        q = create_question(text="Future", days=-1)
        choice = q.choice_set.create(choice_text="1", votes=10)
        self.client.post(reverse('polls:nullask', args=(q.id,)))

        # Update the Python object to reflect changes in the database
        choice.refresh_from_db()

        self.assertEqual(choice.votes, 0)
