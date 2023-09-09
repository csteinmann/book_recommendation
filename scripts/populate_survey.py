"""
Script to populate the survey, question, and choice models of the django app
Questions are heavily inspired by the paper "User Perception of Differences in Recommender
Algorithms" by Michael D. Ekstrand, F. Maxwell Harper, Martijn C. Willemsen, and Joseph A. Konstan
"""
from django.shortcuts import get_object_or_404
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'book_recommendation.settings')

import django

django.setup()

from bookrec.models import Survey, Choice, Question


def populate():
    populate_questions()
    populate_choices()


def add_question(survey, text):
    q = Question()
    q.survey = survey
    q.text = text
    q.save()
    return q


def add_choice(question, text):
    c = Choice()
    c.question = question
    c.text = text
    c.save()
    return c


def populate_choices():
    rotation_list = ['IIUU', 'IIALS', 'UUALS', 'UUII', 'ALSII', 'ALSUU']
    choice_list = ['Much more A than B',
                   'Bit more A than B',
                   'About the same',
                   'Bit more B than A',
                   'Much more B than A']
    for state in rotation_list:
        survey = get_object_or_404(Survey, rotation_state=state)
        for question in survey.question_set.all():
            for choice in choice_list:
                add_choice(question, choice)


def populate_questions():
    rotation_list = ['IIUU', 'IIALS', 'UUALS', 'UUII', 'ALSII', 'ALSUU']
    question_list = ['Based on your first impression, which list do you prefer?',
                     # line for separation
                     'Which list has more books that you find appealing?',
                     'Which list has more books that might be among the best books you read in the next year?',
                     'Which list has more obviously bad book recommendations for you?',
                     'Which recommender does a better job of putting better books at the top?',
                     # line for separation
                     'Which list has more books that are similar to each other?',
                     'Which list has a more varied selection of books?',
                     'Which list has more books that match a wider variety of moods?',
                     'Which list would suit a broader set of tastes?',
                     # line for separation
                     'Which recommender better understands your taste in books?',
                     'Which recommender would you trust to provide you with recommendations?',
                     'Which recommender seems more personalised to your book ratings?',
                     'Which recommender more represents mainstream tastes instead of your own?',
                     # line for separation
                     'Which recommender would better help you find books to watch?',
                     'Which recommender would you be more likely to recommend to your friends',
                     'Which list of recommendations do you find more valuable?',
                     'Which recommender would you rather have as an app on your mobile phone?',
                     'Which recommender would better help to pick satisfactory books?',
                     # line for separation
                     'Which list has more books you do not expect?',
                     'Which list has more books that are familiar to you?',
                     'Which list has more pleasantly surprising books?',
                     'Which list has more books you would not have thought to consider?',
                     'Which list provides fewer new suggestions?']
    for state in rotation_list:
        s = get_object_or_404(Survey, rotation_state=state)
        for question in question_list:
            add_question(s, question)


if __name__ == '__main__':
    print("Starting populating the survey")
    populate()
