import csv
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'book_recommendation.settings')

import django
from asgiref.sync import sync_to_async

django.setup()

from bookrec.models import SurveyResponse

# Get all survey responses
all_rows = list(SurveyResponse.objects.all())

# Open a CSV file for writing
csv_file_path = '../data/survey_response.csv'
with open(csv_file_path, 'w', newline='') as csvfile:
    fieldnames = [field.name for field in SurveyResponse._meta.fields]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Write the data
    for response in all_rows:
        writer.writerow({field.name: getattr(response, field.name) for field in SurveyResponse._meta.fields})



