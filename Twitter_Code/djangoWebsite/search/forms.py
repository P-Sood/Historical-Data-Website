from django import forms

class Search(forms.Form):
    input_ = forms.CharField(label = 'Input',max_length=100, required=True)
    fromDate = forms.CharField(label = 'fromDate',max_length=10, required=False)
    toDate = forms.CharField(label = 'toDate',max_length=10, required=False)

class Query(forms.Form):
    searchDB = forms.CharField(label = "Search", max_length=100,required=True)