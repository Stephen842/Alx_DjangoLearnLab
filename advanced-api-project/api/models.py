from django.db import models
from datetime import datetime

# Create your models here.

class Author(models.Model):
    '''
    Represent an author of one or more books.
    Each author can be linked to multiple book entries.
    '''
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Book(models.Model):
    '''
    Represent a written book.
    Each book belong to one author(one-to-many relationship)
    '''
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} ({self.publication_year})'