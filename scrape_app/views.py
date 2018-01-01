from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
import urllib
from datetime import datetime
import re

from . import forms
from . import models

# Create your views here.
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

            try:
                stored = models.WebPage.objects.get(url=url)
            except:
            # if not stored:
                with urllib.request.urlopen(url) as sock:
                    html = sock.read()
                    soup = BeautifulSoup(html, 'html.parser')
                    # print(soup.prettify())

                tags = set([])
                domain = 'https://' + re.search(r'://(.*?)/', url).group(1)
                for a in soup.find_all('a'):
                    try:
                        a = str(a['href'])

                        # print('\t' + a)
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
                    # if a.startswith('#') or a == '':
                    #     continue
                    # elif a.startswith('/'):
                    #     a = domain + a
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


    """
    You have to deal with the unicode problem!!!!
    Make the result.html look better

    """
