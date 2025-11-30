from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Author, Book


class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='JohnnyDoe', password='Testing123')
        self.client = APIClient()

        # Create Authors
        self.author1 = Author.objects.create(name='Stephen King')
        self.author2 = Author.objects.create(name='J.K. Rowling')

        # Create Books
        self.book1 = Book.objects.create(title='IT', publication_year=1986, author=self.author1)
        self.book2 = Book.objects.create(title='Harry Potter', publication_year=1997, author=self.author2)

        # Login URL for authenticated requests
        self.client.login(username='JohnnyDoe', password='Testing123')


    #------------------- CRUD Operation For Book Model -------------------#
    def test_list_books(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book(self):
        url = reverse('book-detail', kwargs={'pk': self.book1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'IT')

    def test_create_book(self):
        url = reverse('book-create')
        data = {'title': 'Career', 'publication_year': 1974, 'author': self.author1.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_update_book(self):
        url = reverse('book-update', kwargs={'pk': self.book1.id})
        data = {'title': 'Career Update', 'publication_year': 1978, 'author': self.author1.id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Career Update')

    def test_delete_book(self):
        url = reverse('book-delete', kwargs={'pk': self.book2.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)


    #------------------- Filtering, Searching and Ordering Operation -------------------#

    '''
    Filtering by title
    '''
    def test_filter_books_by_title(self):
        url = reverse('book-list') + '?title=IT'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    '''
    Searching by title and author name
    '''
    def test_search_books_by_author_name(self):
        url = reverse('book-list') + '?search=Rowling'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Harry Potter')

    '''
    Ordering by publication_year
    '''
    def test_order_books_by_publication_year_desc(self):
        url = reverse('book-list') + '?ordering=-publication_year'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], '1978')


    #------------------- Permission Test Operation -------------------#
    '''
    Permission enforcement for authenticated vs unauthenticated users
    '''
    def test_create_book_requires_authentication(self):
        self.client.logout()
        url = reverse('book-create')
        data = {"title": "Misery", "publication_year": 1987, "author": self.author1.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

