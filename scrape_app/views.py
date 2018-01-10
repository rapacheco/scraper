from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from bs4 import BeautifulSoup
from datetime import datetime
import urllib
import re

from . import forms
from . import models

# Create your views here.
def register(request):
    """
    """
    registered = False

    if request.method == 'GET':
        d = {'form' : forms.UserForm}
        return render(request, 'scrape_app/register.html', context=d)

    else:
        user_form = forms.UserForm(data=request.POST)
        password = user_form['password'].value()
        confirm = user_form['confirm'].value()

        if user_form.is_valid() and (password == confirm):
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            registered = True
            user_auth = authenticate(username=user.username, password=user.password)
            if user_auth.is_active:
                login(request, user_auth)
            else:
                return HttpResponse("Error, see admin")

            # return render(request, 'scrape_app/index.html', context={'user' : user_auth})
            return HttpResponseRedirect(reverse('index'))
        else:
            print("error")
            return HttpResponse('Sorry :()')

def user_login(request):

    if request.method == 'GET':
        return render(request, 'scrape_app/login.html', context={})

    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user.is_active:
            login(request, user)
        else:
            return HttpResponse("Error, see admin")
        return HttpResponseRedirect(reverse('index'))

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def index(request):
    """
    Main page for the scraper app
    Gets the URL from the user and scrape it for anchor tags
    """
    form = forms.FormURL()

    if request.method == 'POST':
        form = forms.FormURL(request.POST)

        if form.is_valid():
            print("VALID URL!")

            url = form.cleaned_data['url']
            print("URL: " + url)

            tags = set([])
            try:
                stored = models.WebPage.objects.get(url=url)
                print("Data found in database!")
            except:
                print("No data in database")
                with urllib.request.urlopen(url) as sock:
                    html = sock.read()
                    soup = BeautifulSoup(html, 'html.parser')
                try:
                    domain = 'https://' + re.search(r'://(.*?)/', url).group(1)
                except:
                    domain = 'https://' + re.search(r'://(.*?)$', url).group(1)
                for a in soup.find_all('a'):
                    try:
                        a = str(a['href'])
                    except:
                        continue
                    else:
                        if a.startswith('#') or a == '':
                            continue
                        elif a.startswith('/'):
                            a = domain + a
                        tags.add(str(a))
                page = models.WebPage.objects.get_or_create(url=url,
                                                            title=soup.title.string,
                                                            number_of_tags=len(tags))[0]
                page.save()

                for a in tags:
                    new = models.Tag.objects.get_or_create(page=page, tag=a)

                stored = models.WebPage.objects.get(url=url)

            q = models.Tag.objects.filter(page=stored)
            print("Title: " + stored.title)
            print("Anchor tags:")
            for a in q:
                try:
                    print('\t' + str(a))
                except:
                    continue

            print("Number of anchor tags: " + str(stored.number_of_tags))

            return render(request, 'scrape_app/result.html', {'result' : q})

    return render(request, 'scrape_app/index.html', {'form' : form})
