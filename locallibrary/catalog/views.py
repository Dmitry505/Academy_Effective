from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic


def index(request):
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    num_instances_available=\
        BookInstance.objects\
        .filter(status__exact='a')\
        .count()

    num_genre=BookInstance.objects.count()
    num_authors = Author.objects.count()  # The 'all()' is implied by default.

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1


    return render(
        request,
        'index.html',
        context={
            'num_books': num_books, 'num_instances': num_instances,
            'num_instances_available': num_instances_available,
            'num_authors': num_authors,
            'num_visits': num_visits, 'num_genre': num_genre
        },  # num_visits appended
    )


class BookListView(generic.ListView):
    model = Book

class BookDetailView(generic.DetailView):
    model = Book
    paginate_by = 10

class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.DetailView):
    model = Author
    paginate_by = 10
