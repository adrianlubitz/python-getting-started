import requests
from random import shuffle
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model

from .models import Suggestion, Draw


from django import forms

class SuggestForm(forms.Form):
    color = forms.CharField(label='Farbe', max_length=100)
    describtion = forms.CharField(label='Beschreibung', max_length=100)

def get_users():
    # get all users (except admin)
    User = get_user_model()
    users = User.objects.all().exclude(is_superuser=True)
    missing_users = []
    for user in users:
        sug = Suggestion.objects.filter(author=user)
        if len(sug) == 0:
            missing_users.append(str(user))
        elif len(sug) == 1:
            pass
        else:
            raise Exception('invalid state - only one suggestion per user is possible')
    return missing_users

# Create your views here.
def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST': 
        # create a form instance and populate it with data from the request:
        form = SuggestForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # use suggestions to put in db 
            Suggestion.objects.create(color=form.cleaned_data['color'], describtion=form.cleaned_data['describtion'], author=request.user.username)     
            missing_users = get_users()
            if missing_users:
                context={'state':'wait', 'missing_users':missing_users}
            else:
                # make the draws
                colors = []
                describtions = []
                names = []
                suggestions = Suggestion.objects.all()
                for suggestion in suggestions:
                    describtions.append(suggestion.describtion)
                    colors.append(suggestion.color)
                    names.append(suggestion.author)
                # shuffle all lists and always pick the next
                shuffle(colors)
                shuffle(describtions)
                shuffle(names)
                for i, name in enumerate(names):
                    Draw.objects.create(color=colors[i], describtion=describtions[i], recipient=names[i-1], giver=name)
                    if name == request.user.username:
                        recipient = names[i-1]
                        color = colors[i]
                        describtion = describtions[i]
                context = {'state':'draw', 'color':color, 'recipient':recipient, 'describtion':describtion}
        else:
            context = {'state':'invalidForm'}
    else:
        # check db
        sug = Suggestion.objects.filter(author=request.user.username)
        if len(sug) == 0: 
            form = SuggestForm()
            context = {'state':'suggest', 'form':form} # here I transport if I want to show suggest, wait or draw and with which values
        else:
            missing_users = get_users()
            if missing_users:
                context={'state':'wait', 'missing_users':missing_users}
            else:
                draw = Draw.objects.get(pk=request.user.username)
                context = {'state':'draw', 'color':draw.color, 'recipient':draw.recipient, 'describtion':draw.describtion}
    return render(request, 'index.html', context)



