# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response

from django import forms

class UserForm(forms.Form):
    username = forms.CharField()

def regist(req):
    if req.method == "POST":
        uf = UserForm(req.POST)
        if uf.is_valid():
            print uf.cleaned_data['username']
            return HttpResponse('ok')
    else:
        uf = UserForm()
    return render_to_response('regist.html',{'uf':uf})
