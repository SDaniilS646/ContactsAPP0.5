from django.http import HttpResponse
from django.shortcuts import render

from .menu import MAIN_TABS

def home(request):

  return render(request, 'home.html')

def delete_el():
  pass