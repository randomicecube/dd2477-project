from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from django.conf import settings
from .forms import SearchForm
from utils.ElasticSearch import create_elasticsearch_client, create_index, index_news_articles
from utils.search import build_query
from utils.sqlitedb import save_user_profile, load_user_profile
import requests, os


DATA_FILE = "data/News_Category_Dataset_v3.json"

client = create_elasticsearch_client()
index_name = "news_articles"

create_index(client, index_name)

# In server mode, we always index the news articles
index_news_articles(client, index_name, DATA_FILE)


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
  """
  # Get the query from the form
  form = SearchForm(request.GET)
  if not form.is_valid():
    return render(request, 'engine/index.html', {
      'form': SearchForm(),
    })

  query = form.cleaned_data['query']
  query_type = form.cleaned_data['query_type']

  # Log the search query
  username = request.user.username
  profile = load_user_profile(username)
  profile.add_search_query(query)

  query = build_query(query_type, query)

  # Personalize the query based on user profile
  query = profile.personalize_search(query)

  # Perform the search
  response = client.search(index=index_name, body=query)
  # Get the entries from the response
  entries = response['hits']['hits']

  save_user_profile(profile)

  # Do something with them -- have the query type into account with regards with the ordering
  return render(request, 'engine/list-entries.html', {
    'entries': entries
  })

def log_entry_click(request):
  """
  When a user clicks on an entry (i.e., expands a row), we want to log that event
  """
  if request.method == 'POST' and request.is_ajax():
      entry_id = request.POST.get('entry_id')
      
      clicked_category = request.POST.get('clicked_category')
      username = request.user.username
      profile = load_user_profile(username)
      profile.add_click_history(clicked_category)
      save_user_profile(profile)
      
      return JsonResponse({'success': True})
  else:
      return JsonResponse({'success': False})
