from django import forms

# Macros for lengths - easier to edit them this way
LENGTH_QUERY = 256

QUERY_TYPES = [
  ('intersection', 'Intersection'),
  ('phrase', 'Phrase'),
  ('ranked', 'Ranked')
]

# Form used for creating a new paper
class SearchForm(forms.Form):
  query = forms.CharField(max_length=LENGTH_QUERY, required=True)
  query_type = forms.ChoiceField(choices=QUERY_TYPES, required=True)
