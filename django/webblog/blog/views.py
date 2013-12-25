from blog.models import * 
from django.shortcuts import render_to_response 
from django.template import Context, loader 
from django.http import HttpResponse 

def index(request): 
    article_list = Article.objects.all() 
    return render_to_response('index.html', {'article_list': article_list})
