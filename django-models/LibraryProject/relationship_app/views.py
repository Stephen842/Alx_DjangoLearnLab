from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import user_passes_test, login_required
from .forms import RegisterForm
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


# User Registration
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user
            return redirect('list_books')
    else:
        form = UserCreationForm()

    context = {
        'form': form,
    }

    return render(request, 'relationship_app/register.html', context)

# User Login
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('list_books')
    else:
        form = AuthenticationForm()

    context = {
        'form': form,
    }

    return render(request, 'relationship_app/login.html', context)

# User Logout
def logout_view(request):
    logout(request)
    return render(request, 'relationship_app/logout.html')

# Helper checks
def is_admin(user):
    return user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.userprofile.role == 'Librarian'

def is_member(user):
    return user.userprofile.role == 'Member'


@login_required
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')


@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')


@login_required
@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')