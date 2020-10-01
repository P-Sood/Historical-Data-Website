from django.shortcuts import render
from .forms import NewsInput
from .tasks import NewScraper

# Create your views here.

def ScrapeNews(request):
    homeHTML = 'Scraper/NewsScraper.html'

    Inputform = NewsInput()

    if request.method == 'POST':
        Inputform = NewsInput(request.POST)
        if Inputform.is_valid():
            input_ = Inputform.cleaned_data['input_']
            NewScraper(input_)
    context = {
        'Inputform': Inputform,
    }

    return render(request,homeHTML,context)