from django import forms

class Search(forms.Form):
    query = forms.CharField(label = 'Search ',max_length=100, required=True)
    fromDate = forms.CharField(label = 'Search ',max_length=11, required=False)
    toDate = forms.CharField(label = 'Search ',max_length=11, required=False)