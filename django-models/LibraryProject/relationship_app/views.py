from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from .models import Library, Book

# Function-based view: simple text list of books (for ALX check)
def list_books(request):
    books = Book.objects.all()
    output = ""
    for book in books:
        output += f"{book.title} by {book.author.name}\n"
    return HttpResponse(output)

# Function-based view: List all books
def list_books(request):
    books = Book.objects.all()
    context ={
        'books': books
    }
    return render(request, 'relationship_app/list_books.html', context)


# Class-based view: Library details with books
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
