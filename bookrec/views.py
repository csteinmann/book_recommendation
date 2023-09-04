from django.http import HttpResponse
from django.shortcuts import render
from bookrec.models import Book
# Create your views here.


def index(request):
    context_dict = {}
    book_list = Book.objects.order_by('publication_year')[:10] # PLACEHOLDER
    context_dict['books_ii'] = book_list
    context_dict['books_uu'] = book_list
    context_dict['books_svd'] = book_list
    context_dict['books_nn'] = book_list

    return render(request, 'bookrec/index.html', context_dict)
