from rest_framework import serializers
from datetime import datetime
from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    '''
    Serialize book objects, including validation to prevent
    future publication year
    '''

    class Meta:
        model = Book
        fields = '__all__'

    # Custom validation
    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError('Publication year cannot be in the future')
        return value
    

class AuthorSerializer(serializers.ModelSerializer):
    '''
    Serialize Author objects and add nests all related Book entries
    using the BookSerializer
    '''

    books = BookSerializer(many=True, read_only=True)
    # related_name='books' makes this work

    class Meta:
        model = Author
        fields = ['name', 'books']