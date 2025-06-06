import datetime
import uuid

# Get user model from settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    Permission,
)  # Required to grant the permission needed to set a book as returned.
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from catalog.models import Author, Book, BookInstance, Genre, Language


class AuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_authors = 13

        for author_id in range(number_of_authors):
            Author.objects.create(
                first_name=f"Dominique {author_id}",
                last_name=f"Surname {author_id}",
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/catalog/authors/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("authors"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("authors"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/author_list.html")


User = get_user_model()


class LoanedBookInstancesByUserListViewTest(TestCase):
    def setUp(self):
        # Create two users
        test_user1 = User.objects.create_user(
            username="testuser1", password="1X<ISRUkw+tuK"
        )
        test_user2 = User.objects.create_user(
            username="testuser2", password="2HJ1vRV0Z&3iD"
        )

        test_user1.save()
        test_user2.save()

        # Create a book
        test_author = Author.objects.create(
            first_name="John", last_name="Smith"
        )

        test_language = Language.objects.create(name="English")
        test_book = Book.objects.create(
            title="Book Title",
            summary="My book summary",
            isbn="ABCDEFG",
            author=test_author,
            language=test_language,
        )

        # Create genre as a post-step
        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(
            genre_objects_for_book
        )  # Direct assignment of many-to-many types not allowed.
        test_book.save()

        # Create 30 BookInstance objects
        number_of_book_copies = 30
        for book_copy in range(number_of_book_copies):
            return_date = timezone.localtime() + datetime.timedelta(
                days=book_copy % 5
            )
            the_borrower = test_user1 if book_copy % 2 else test_user2
            status = "m"
            BookInstance.objects.create(
                book=test_book,
                imprint="Unlikely Imprint, 2016",
                due_back=return_date,
                borrower=the_borrower,
                status=status,
            )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("my-borrowed"))
        self.assertRedirects(
            response, "/accounts/login/?next=/catalog/mybooks/"
        )

    def test_logged_in_uses_correct_template(self):
        self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        response = self.client.get(reverse("my-borrowed"))

        # Check our user is logged in
        self.assertEqual(str(response.context["user"]), "testuser1")
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(
            response, "catalog/bookinstance_list_borrowed_user.html"
        )


class RenewBookInstancesViewTest(TestCase):
    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(
            username="testuser1", password="1X<ISRUkw+tuK"
        )
        test_user2 = User.objects.create_user(
            username="testuser2", password="2HJ1vRV0Z&3iD"
        )

        test_user1.save()
        test_user2.save()

        # Give test_user2 permission to renew books.
        permission = Permission.objects.get(name="Set book as returned")
        test_user2.user_permissions.add(permission)
        test_user2.save()

        # Create a book
        test_author = Author.objects.create(
            first_name="John", last_name="Smith"
        )

        test_language = Language.objects.create(name="English")
        test_book = Book.objects.create(
            title="Book Title",
            summary="My book summary",
            isbn="ABCDEFG",
            author=test_author,
            language=test_language,
        )

        # Create genre as a post-step
        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(
            genre_objects_for_book
        )  # Direct assignment of many-to-many types not allowed.
        test_book.save()

        # Create a BookInstance object for test_user1
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance1 = BookInstance.objects.create(
            book=test_book,
            imprint="Unlikely Imprint, 2016",
            due_back=return_date,
            borrower=test_user1,
            status="o",
        )

        # Create a BookInstance object for test_user2
        return_date = datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance2 = BookInstance.objects.create(
            book=test_book,
            imprint="Unlikely Imprint, 2016",
            due_back=return_date,
            borrower=test_user2,
            status="o",
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(
            reverse(
                "renew-book-librarian",
                kwargs={"pk": self.test_bookinstance1.pk},
            )
        )
        # Manually check redirect (Can't use assertRedirect,
        # because the redirect URL is unpredictable)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_forbidden_if_logged_in_but_not_correct_permission(self):
        self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        response = self.client.get(
            reverse(
                "renew-book-librarian",
                kwargs={"pk": self.test_bookinstance1.pk},
            )
        )
        self.assertEqual(response.status_code, 302)

    def test_logged_in_with_permission_borrowed_book(self):
        self.client.login(username="testuser2", password="2HJ1vRV0Z&3iD")
        response = self.client.get(
            reverse(
                "renew-book-librarian",
                kwargs={"pk": self.test_bookinstance2.pk},
            )
        )

        # Check that it lets us login - this is our book and we have
        # the right permissions.
        self.assertEqual(response.status_code, 200)

    def test_logged_in_with_permission_another_users_borrowed_book(self):
        self.client.login(username="testuser2", password="2HJ1vRV0Z&3iD")
        response = self.client.get(
            reverse(
                "renew-book-librarian",
                kwargs={"pk": self.test_bookinstance1.pk},
            )
        )

        # Check that it lets us login. We're a librarian, so we can view
        # any users book
        self.assertEqual(response.status_code, 200)

    def test_HTTP404_for_invalid_book_if_logged_in(self):
        # unlikely UID to match our bookinstance!
        test_uid = uuid.uuid4()
        self.client.login(username="testuser2", password="2HJ1vRV0Z&3iD")
        response = self.client.get(
            reverse("renew-book-librarian", kwargs={"pk": test_uid})
        )
        self.assertEqual(response.status_code, 404)

    def test_uses_correct_template(self):
        self.client.login(username="testuser2", password="2HJ1vRV0Z&3iD")
        response = self.client.get(
            reverse(
                "renew-book-librarian",
                kwargs={"pk": self.test_bookinstance1.pk},
            )
        )
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, "catalog/book_renew_librarian.html")

    def test_form_renewal_date_initially_has_date_three_weeks_in_future(self):
        self.client.login(username="testuser2", password="2HJ1vRV0Z&3iD")
        response = self.client.get(
            reverse(
                "renew-book-librarian",
                kwargs={"pk": self.test_bookinstance1.pk},
            )
        )
        self.assertEqual(response.status_code, 200)

        date_3_weeks_in_future = datetime.date.today() + datetime.timedelta(
            weeks=3
        )
        self.assertEqual(
            response.context["form"].initial["renewal_date"],
            date_3_weeks_in_future,
        )

    def test_form_invalid_renewal_date_past(self):
        self.client.login(username="testuser2", password="2HJ1vRV0Z&3iD")
        date_in_past = datetime.date.today() - datetime.timedelta(weeks=1)
        response = self.client.post(
            reverse(
                "renew-book-librarian",
                kwargs={"pk": self.test_bookinstance1.pk},
            ),
            {"renewal_date": date_in_past},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "renewal_date",
            "Invalid date - renewal in past",
        )

    def test_form_invalid_renewal_date_future(self):
        self.client.login(username="testuser2", password="2HJ1vRV0Z&3iD")
        invalid_date_in_future = datetime.date.today() + datetime.timedelta(
            weeks=5
        )
        response = self.client.post(
            reverse(
                "renew-book-librarian",
                kwargs={"pk": self.test_bookinstance1.pk},
            ),
            {"renewal_date": invalid_date_in_future},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "renewal_date",
            "Invalid date - renewal more than 4 weeks ahead",
        )
