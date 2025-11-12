from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from .models import Book
from .forms import ExampleForm

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'pages/book_list.html', {'books': books})


@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = ExampleForm()

    context = {
        'form': form,
    }
    return render(request, 'bookshelf/form_example.html', context)


@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.description = request.POST.get('description')
        book.save()
        return redirect('book_list')
    return render(request, 'pages/book_form.html', {'book': book})


@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect('book_list')


def search_books(request):
    query = request.GET.get('q', '')
    books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
    context ={
        'books': books,
    }
    return render(request, 'bookshelf/book_list.html', context)