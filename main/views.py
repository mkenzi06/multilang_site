from django.shortcuts import render
from .models import Article
# Create your views here.
def home(request):
    return render(request, 'main/home.html')
def articles_list(request):
    articles = Article.objects.all().order_by('date')
    return render(request, 'main/articles_list.html', {'articles': articles})
