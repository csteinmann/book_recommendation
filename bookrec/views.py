from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from bookrec.models import Book, Survey
from bookrec.forms import SurveyForm
import csv
import os
from pathlib import Path
import pickle

BASE_DIR = Path(__file__).resolve().parent.parent


# Create your views here.

def index(request):

    # Create entries for the book list using our helper function
    books_ii = read_csv_recs(os.path.join(BASE_DIR, 'data/recs_ii.csv'))
    books_uu = read_csv_recs(os.path.join(BASE_DIR, 'data/recs_uu.csv'))
    books_als = read_csv_recs(os.path.join(BASE_DIR, 'data/recs_als.csv'))

    book_list = [books_ii, books_uu, books_als]

    # open pickle to receive current rotation state
    with open('rotator_pickle.pk', 'rb') as fi:
        current_rotation_list = pickle.load(fi)
        rotation_state = current_rotation_list[0]

    # search current rotation state and create content dictionary accordingly
    # also call the function to initiate the rotation of the state list
    if rotation_state == 'IIUU':
        context_dict = {'rotation_state': rotation_state, 'books_a': book_list[0], 'books_b': book_list[1]}
        rotate_content_list()
        return render(request, 'bookrec/index.html', context_dict)
    elif rotation_state == 'IIALS':
        context_dict = {'rotation_state': rotation_state, 'books_a': book_list[0], 'books_b': book_list[2]}
        rotate_content_list()
        return render(request, 'bookrec/index.html', context_dict)
    elif rotation_state == 'UUALS':
        context_dict = {'rotation_state': rotation_state, 'books_a': book_list[1], 'books_b': book_list[2]}
        rotate_content_list()
        return render(request, 'bookrec/index.html', context_dict)
    elif rotation_state == 'UUII':
        context_dict = {'rotation_state': rotation_state, 'books_a': book_list[1], 'books_b': book_list[0]}
        rotate_content_list()
        return render(request, 'bookrec/index.html', context_dict)
    elif rotation_state == 'ALSII':
        context_dict = {'rotation_state': rotation_state, 'books_a': book_list[2], 'books_b': book_list[0]}
        rotate_content_list()
        return render(request, 'bookrec/index.html', context_dict)
    elif rotation_state == 'ALSUU':
        context_dict = {'rotation_state': rotation_state, 'books_a': book_list[2], 'books_b': book_list[1]}
        rotate_content_list()
        return render(request, 'bookrec/index.html', context_dict)


def rotate_content_list():
    with open('rotator_pickle.pk', 'rb') as fi:
        current_rotation_list = pickle.load(fi)
    current_rotation_list.append(current_rotation_list[0])
    del current_rotation_list[0]
    with open('rotator_pickle.pk', 'wb') as fi:
        pickle.dump(current_rotation_list, fi)


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
