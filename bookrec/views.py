import string

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from bookrec.models import Book, Survey, Question, Choice, Submission
from bookrec.forms import SurveyForm
import csv
import os
from pathlib import Path
import pickle

BASE_DIR = Path(__file__).resolve().parent.parent


# Create your views here.

def index(request):
    # Initial context_dict (resolves recommendation lists and rotation)
    context_dict = create_context_dict()
    # Code for handling the survey
    # Get the current rotation state with function
    current_rotation_state = get_current_rotation_state('rotator_pickle.pk')
    # access survey through the rotation_state
    survey = get_object_or_404(Survey, rotation_state=current_rotation_state)
    form = SurveyForm(survey)

    # add form and survey to the context_dict
    context_dict['survey'] = survey
    context_dict['form'] = form

    # IMPORTANT! Rotate the rotation_list; how? look at the docstring inside the function
    rotate_rotation_list('rotator_pickle.pk')

    # return render
    return render(request, 'bookrec/index.html', context_dict)


def thank_you_view(request):
    return render(request, 'bookrec/thank_you.html')


def create_context_dict() -> dict:
    """
    Creates part of the context_dict for the render statement of index.
    """
    # Create entries for the book list using our helper function
    books_ii = read_csv_recs(os.path.join(BASE_DIR, 'data/recs_ii.csv'))
    books_uu = read_csv_recs(os.path.join(BASE_DIR, 'data/recs_uu.csv'))
    books_als = read_csv_recs(os.path.join(BASE_DIR, 'data/recs_als.csv'))

    # Line below is only needed for the first run to create the pickled file!
    # initiate_pickle('rotator_pickle-pk')

    # Open the pickled file to read the rotation list and save the rotation state
    current_rotation_state = get_current_rotation_state('rotator_pickle.pk')

    # Look for current rotation state and create content dictionary accordingly
    # Returns the created context_dict
    if current_rotation_state == 'IIUU':
        context_dict = {'books_a': books_ii, 'books_b': books_uu}
        return context_dict
    elif current_rotation_state == 'IIALS':
        context_dict = {'books_a': books_ii, 'books_b': books_als}
        return context_dict
    elif current_rotation_state == 'UUALS':
        context_dict = {'books_a': books_uu, 'books_b': books_als}
        return context_dict
    elif current_rotation_state == 'UUII':
        context_dict = {'books_a': books_uu, 'books_b': books_ii}
        return context_dict
    elif current_rotation_state == 'ALSII':
        context_dict = {'books_a': books_als, 'books_b': books_ii}
        return context_dict
    elif current_rotation_state == 'ALSUU':
        context_dict = {'books_a': books_als, 'books_b': books_uu}
        return context_dict


def get_current_rotation_state(filename) -> string:
    """Reads the pickled rotation string
    and returns the current rotation state: first element of list
    :param filename: filename of pickle"""
    with open(filename, 'rb') as fi:
        current_rotation_list = pickle.load(fi)
        current_rotation_state = current_rotation_list[0]
        return current_rotation_state


def initiate_pickle(filename):
    """Needed for the initiation of the pickled file
    Creates a pickle with the start rotation
    :param filename: filename of pickle"""
    rotation_list = ['IIUU', 'IIALS', 'UUALS', 'UUII', 'ALSII', 'ALSUU']
    with open(filename, 'wb') as fi:
        pickle.dump(rotation_list, fi)


def rotate_rotation_list(filename):
    """Rotates the State list: [a, b, c] -> [b, c, a]
    :param filename: filename of pickle
    """
    with open(filename, 'rb') as fi:
        current_rotation_list = pickle.load(fi)
    current_rotation_list.append(current_rotation_list[0])
    del current_rotation_list[0]
    with open(filename, 'wb') as fi:
        pickle.dump(current_rotation_list, fi)


def read_csv_recs(path) -> list:
    """Reads a csv file at the specified path.
    :param path: path to file
    Returns a list consisting of recommended Books extracted by their ID"""
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
