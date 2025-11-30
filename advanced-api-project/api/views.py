from django.shortcuts import render
from django_filters import rest_framework
from rest_framwork import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    '''
    Lists all books.
    Accessible to everyone(read-only)
    '''

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permissions_classes = [IsAuthenticatedOrReadOnly]

    # Enable filtering, searching, ordering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Filter by fields
    filterset_fields = ['title', 'publication_year', 'author']

    # Search by title or author's name
    search_fields = ['title', 'author__name']

    # Allow ordering by title or publication_year
    ordering_fields = ['title', 'publication_year']

    # Default Ordering
    ordering = ['title']


class BookDetailView(generics.RetrieveAPIView):
    '''
    Lists a single book by it ID.
    Read-only for unauthenticated users.
    '''

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permissions_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    '''
    Create a new book entry.
    Only authenticated users can create books.
    DRF handles validation through the serializer
    '''

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permissions_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    '''
    Update an existing book entry.
    Only authenticated users can update books.
    '''

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permissions_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    '''
    Delete a book entry.
    Only authenticated users can delete books.
    '''

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permissions_classes = [IsAuthenticated]