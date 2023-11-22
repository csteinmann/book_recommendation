"""
Access the survey data from the database excluding age_group under 18 due to ethical considerations.
The csv file will contain a column for each demographic information and a column for every question (24*6=144).
The dataframe will be cleaned and compressed in another file
"""


import csv
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'book_recommendation.settings')

import django

django.setup()

from bookrec.models import SurveyResponse, Question

# Get all survey responses
filtered_rows = SurveyResponse.objects.exclude(age_group="Under 18")

# Open a CSV file for writing with survey response and corresponding question and choice data
csv_file_path = '../data/survey_response_raw.csv'
with open(csv_file_path, 'w', newline='') as csvfile:
    fieldnames = ['SurveyResponseID', 'rotation_state', 'age_group', 'gender', 'reading_platform', 'book_frequency',
                  'genre', 'sessionId']

    # Add fields for each question
    for question in Question.objects.all():
        fieldnames.append(f"answer_to_{question.id}")

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Write the data
    for response in filtered_rows:
        row_data = {
            'SurveyResponseID': response.id,
            'rotation_state': response.rotation_state,
            'age_group': response.age_group,
            'gender': response.gender,
            'reading_platform': response.reading_platform,
            'book_frequency': response.book_frequency,
            'genre': response.genre,
            'sessionId': response.sessionId,
        }

        # Fetch and add the answers for each question using the many-to-many relationship
        for question in Question.objects.all():
            try:
                # Get the first choice associated with the question for the current response
                choice = response.answer.filter(question=question).first()
                row_data[f"answer_to_{question.id}"] = choice.text if choice else None
            except SurveyResponse.DoesNotExist:
                row_data[f"answer_to_{question.id}"] = None

        writer.writerow(row_data)



