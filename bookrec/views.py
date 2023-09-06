from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from bookrec.models import Book, Survey
from bookrec.forms import SurveyForm
import csv
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


# Create your views here.

def index(request):
    # Create context_dict using our helper function
    context_dict = {'books_ii': read_csv_recs(os.path.join(BASE_DIR, 'data/recs_ii.csv')),
                    'books_uu': read_csv_recs(os.path.join(BASE_DIR, 'data/recs_uu.csv')),
                    'books_als': read_csv_recs(os.path.join(BASE_DIR, 'data/recs_als.csv'))}

    return render(request, 'bookrec/index.html', context_dict)


def read_csv_recs(path):
    # Read the csv file at the specified path
    data_reader = csv.reader(open(path, encoding='utf-8'), delimiter=',', quotechar='"')
    # Skip first line to avoid the column names
    next(data_reader)
    # Create the book list used for the context_dict
    book_list = []
    # Iterate over the rows and append the recommended book by the unique id to the book list
    # We use objects.get instead of filter because id is a unique attribute
    for row in data_reader:
        book_list.append(Book.objects.get(book_id=row[1]))
    return book_list


def show_survey(request, id=None):
    survey = get_object_or_404(Survey, pk=id)
    form = SurveyForm(survey)

    context = {
        'survey': survey,
        'form': form,
    }
    return render(request, 'bookrec/survey.html', context)
