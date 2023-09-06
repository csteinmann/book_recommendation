"""Script for populating the db.sqlite3 database with the desired data form the following data set:
https://mengtingwan.github.io/data/goodreads.html#datasets specifically the goodreads_books.json.gz file
(~2gb, about 2.3m books). The mentioned file has to be unzipped, converted to a csv file and placed in the data
folder at the manage.py level to work properly.
"""

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'book_recommendation.settings')

import django

django.setup()

from bookrec.models import Book
import csv


def run():
    data_reader = csv.reader(open('/data/df_books.csv', encoding="utf8"),
                             delimiter=',', quotechar='"')
    next(data_reader)
    Book.objects.all().delete()

    for row in data_reader:
        print(row)
        book = Book(book_id=row[0])
        book.title_without_series = row[1]
        book.book_description = row[2]
        book.publication_year = row[3]
        book.publisher = row[4]
        book.book_average_rating = row[6]
        book.cover_page = row[7]
        book.book_url = row[8]
        book.save()


if __name__ == '__main__':
    print('Starting bookrec population script...')
    run()