import string
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from bookrec.models import Book, Survey, RotationState
from bookrec.forms import CombinedForm, DemographicForm
import csv
import os
from pathlib import Path
import logging

# Base directory - used for reading and saving data - avoiding hardcoding the paths
BASE_DIR = Path(__file__).resolve().parent.parent
logger = logging.getLogger('BookRec')


# Create your views here.

def index_view(request):
    """View for the index page and demographic data of the participant"""
    # Receive post data if request.method is Post id not post_data is None
    post_data = request.POST if request.method == 'POST' else None
    # Create the demographic form
    demographic_form = DemographicForm(post_data)
    # Check if the form is valid
    if demographic_form.is_valid():
        # Save the post data in a session to access it later in survey_view
        request.session['demographic_data'] = demographic_form.cleaned_data
        # Print a message that the submission was saved
        messages.add_message(request, messages.INFO, 'Submissions saved.')
        # redirect to the research scenario page
        return redirect('bookrec_app:research_scenario')
    # return render
    return render(request, 'bookrec/index.html', context={'demographic_form': demographic_form})


def research_scenario_view(request):
    """View for the description of the research scenario"""
    return render(request, 'bookrec/research_scenario.html', context={})


def survey_view(request):
    """Handles the program and render logic for the survey page (main part of website)"""
    # Initial context_dict (resolves recommendation lists and rotation)
    context_dict = create_context_dict()
    # Get the current rotation state with function
    current_rotation_state = get_current_rotation_state()
    # access survey through the rotation_state
    current_survey = get_object_or_404(Survey, rotation_state=current_rotation_state)
    # get the form data
    post_data = request.POST if request.method == 'POST' else None
    # retrieve the demographic data from the session
    demographic_data = request.session.get('demographic_data', {})
    # retrieve the sessionId created by html field and set by javascript in logging.js
    sessionId = request.POST.get('sessionId') if request.method == 'POST' else None
    # create initial data dictionary containing the sessionId and the DemographicData from index view
    initial_data = {
        'sessionId': sessionId,
        **demographic_data
    }
    # create a combinedForm with both initial_data and survey data
    combined_form = CombinedForm(current_survey, post_data, initial=initial_data)
    if combined_form.is_valid():
        # save submission
        combined_form.save()
        # display message that the submission was saved
        messages.add_message(request, messages.INFO, 'Submissions saved.')
        # redirect to thank you page !important!
        return redirect('bookrec_app:thank_you')

    # add form and survey to the context_dict
    context_dict['survey'] = current_survey
    context_dict['survey_form'] = combined_form

    # return render
    return render(request, 'bookrec/survey_page.html', context_dict)


def thank_you_view(request):
    """Handles program and render logic for the thank-you page - accessed when filling out the survey and
    successfully saving the data entered by the participant"""

    # IMPORTANT! Rotate the rotation_list; how? look at the docstring inside the function
    rotate_rotation_list()
    # Return render
    return render(request, 'bookrec/thank_you.html')


def logging_view(request):
    """Handles the logger messages received by the json logger"""
    if request.method == "POST":
        message = request.POST.get("message")
        logger.info(f"User Interaction: {message}")
        return JsonResponse({"status": "ok"})
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"})


def create_context_dict() -> dict:
    """Creates part of the context_dict for the render statement of index."""
    # Create entries for the book list using our helper function
    books_ii = read_csv_recs(os.path.join(BASE_DIR, 'data/recs_ii.csv'))
    books_uu = read_csv_recs(os.path.join(BASE_DIR, 'data/recs_uu.csv'))
    books_als = read_csv_recs(os.path.join(BASE_DIR, 'data/recs_als.csv'))

    # Open the pickled file to read the rotation list and save the rotation state
    current_rotation_state = get_current_rotation_state()

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


def get_current_rotation_state() -> string:
    """Retrieves the current rotation state form the database by using the function of the model"""
    rotation_state = RotationState.objects.first()
    return rotation_state.get_current_state()


def rotate_rotation_list():
    """Changes the index in the rotation state model which results in accessing the next rotation abbr.
    in the next webpage call"""
    rotation_state = RotationState.objects.first()
    current_index = rotation_state.current_index
    rotation_order = rotation_state.rotation_order
    # set the new index
    new_index = (current_index + 1) % len(rotation_order)
    rotation_state.current_index = new_index
    rotation_state.save()
    return


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
