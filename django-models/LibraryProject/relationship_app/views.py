from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.decorators import permission_required
from .forms import RegisterForm
from .models import Library, Book, UserProfile

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


@permission_required('relationship_app.can_add_book')
def add_book(request):
    return render(request, 'relationship_app/add_book.html')

@permission_required('relationship_app.can_change_book')
def edit_book(request):
    return render(request, 'relationship_app/edit_book.html')

@permission_required('relationship_app.can_delete_book')
def delete_book(request):
    return render(request, 'relationship_app/delete_book.html')

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

def Admin(user):
    """
    Check if user is authenticated and has 'admin' role.
    Only users with the 'Admin' role can access admin views.
    """
    # Check if user is authenticated first
    if not user.is_authenticated:
        return False
    # Safely check if user has a profile and if the role is 'admin'
    try:
        return user.profile.role == 'admin'
    except UserProfile.DoesNotExist:
        # User doesn't have a profile
        return False
@user_passes_test(Admin)
def admin_dashboard(request):
    return render(request, 'relationship_app/admin_view.html')


def Librarian(user):
    return hasattr(user, 'profile') and user.profile.role == 'librarian'
@user_passes_test(Librarian)
def librarian_dashboard(request):
    return render(request, 'relationship_app/librarian_view.html')


def Member(user):
    return hasattr(user, 'profile') and user.profile.role == 'member'
@user_passes_test(Member)
def member_dashboard(request):
    return render(request, 'relationship_app/member_view.html')
