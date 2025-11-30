from django.shortcuts import render
from rest_framwork import generics, permissions
from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    '''
    Lists all books.
    Accessible to everyone(read-only)
    '''

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permissions_classes = [permissions.AllowAny]


class BookDetailView(generics.RetrieveAPIView):
    '''
    Lists a single book by it ID.
    Read-only for unauthenticated users.
    '''

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permissions_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):
    '''
    Create a new book entry.
    Only authenticated users can create books.
    DRF handles validation through the serializer
    '''

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    '''
    Update an existing book entry.
    Only authenticated users can update books.
    '''

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permissions_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    '''
    Delete a book entry.
    Only authenticated users can delete books.
    '''

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permissions_classes = [permissions.IsAuthenticated]