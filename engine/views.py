from django.shortcuts import render
import requests, os
from .forms import SearchForm
from django.http import HttpRequest
from django.conf import settings

ENTRIES_ENDPOINT = os.getenv('ENTRIES_ENDPOINT') # TODO: make this something

PAGE_SIZE = 10

def index(request):
  """
  Renders the homepage
  """
  return render(request, 'engine/index.html', {
    'form': SearchForm()
  })

def list_entries(request):
  """
  Renders the entries which match the search query
  TODO: still a placeholder, for the time being
  """
  # Get the query from the form
  form = SearchForm(request.GET)
  if not form.is_valid():
    return render(request, 'engine/index.html', {
      'form': form
    })

  query = form.cleaned_data['query']

  # TODO: this is a placeholder, it's here that some of the connection between frontend and backend will happen
  # Get the entries from the API
  response = requests.get(ENTRIES_ENDPOINT, params={
    'query': query,
    'page_size': PAGE_SIZE
  })

  # Check if the request was successful
  if response.status_code != 200:
    return render(request, 'engine/index.html', {
      'form': form,
      'error': 'Failed to get entries from the API'
    })

  # Get the entries from the response
  entries = response.json()

  return render(request, 'engine/list_entries.html', {
    'form': form,
    'entries': entries
  })

def display_entry(request):
  """
  Renders a specific entry
  # TODO: how do we identify it? filename? I don't think there's an ID
  """

  # NOTE: for the time being, as a placeholder, we'll just use the filename
  filename = request.GET.get('filename')
  if not filename:
    return render(request, 'engine/index.html', {
      'form': SearchForm(),
      'error': 'No filename provided'
    })

  # Get the entry from the API
  response = requests.get(ENTRIES_ENDPOINT + filename)

  # Check if the request was successful
  if response.status_code != 200:
    return render(request, 'engine/index.html', {
      'form': SearchForm(),
      'error': 'Failed to get entry from the API'
    })

  return render(request, 'engine/display-entry.html', {
    'entry': response.json(),
    'form': SearchForm()
  })
