"""
Code relict which was used to populate the database with one book to test out the model configuration.
Won't work anymore due to changes in the book model. (attributes and names were changed).
Is easily fixed by changing the names of the attributes if desired.
"""

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'book_recommendation.settings')

import django

django.setup()

from bookrec.models import Book


def populate():
    first_book_item_item = {
        'title': 'Film technique and Film acting',
        'rating': 4.5,
        'author': 'V.I. Pudovkin',
        'image': 'http://books.google.com/books/content?id=IKbBbMxeJDEC&printsec=frontcover&img=1&zoom=1&source=gbs_api',
        'publisher': 'Sims Press',
        'year_published': 2008,
        'categories': 'Drama'}

    b = add_book(title=first_book['title'], author=first_book['author'], rating=first_book['rating'],
                 image=first_book['image'], publisher=first_book['publisher'], year_published=first_book['year_published'],
                 categories=first_book['categories'])


def add_book(title, rating, author, image, publisher, year_published, categories):
    b = Book.objects.get_or_create(title=title)[0]
    b.rating = rating
    # b.description = description
    b.author = author
    b.image = image
    b.publisher = publisher
    b.year_published = year_published
    b.categories = categories
    b.save()
    return b

