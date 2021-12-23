from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from random import choice
from markdown2 import Markdown

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, name):
    entry = util.get_entry(name)
    if entry == None:
        return render(request, "encyclopedia/error.html", {
            "message": "The page for {name} does not exist yet.".format(name=name)
        })
    markdown = Markdown()
    return render(request, "encyclopedia/entry.html", {
        "name": name,
        "entry": markdown.convert(entry)
    })

def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html")

    if request.method == "POST":
        if util.get_entry(request.POST["name"]):
            return render(request, "encyclopedia/error.html", {
                "message" : "This page already exists."
            })
        util.save_entry(request.POST["name"], request.POST["entry"])
        url = reverse('entry', kwargs={'name': request.POST["name"]})
        return HttpResponseRedirect(url)

def edit(request):
    if request.method == "GET":
        return render(request, "encyclopedia/edit.html")
    
    if request.method == "POST":
        if util.get_entry(request.POST["action"]) == "edit":
            return render(request, "encyclopedia/edit.html", {
                "name" : request.POST["name"],
                "etry" : request.POST["entry"]
            })
        elif util.get_entry(request.POST["action"]) == "save":
            util.save_entry(request.POST["name"], request.POST["entry"])
            url = reverse('entry', kwargs={'name': request.POST["name"]})
            return HttpResponseRedirect(url)

def edit(request):
    if request.method == "GET":
        return render(request, "encyclopedia/edit.html")

    if request.method == "POST":
        if request.POST["action"] == "edit":
            return render(request, "encyclopedia/edit.html", {
                "name" : request.POST["name"],
                "entry" : util.get_entry(request.POST["name"])
            })

        elif request.POST["action"] == "save":
            util.save_entry(request.POST["name"], request.POST["entry"])
            url = reverse('entry', kwargs={'name': request.POST["name"]})
            return HttpResponseRedirect(url)

def random_entry(request):
    entry = choice(util.list_entries())
    url = reverse('entry', kwargs={'name': entry})
    return HttpResponseRedirect(url)

def search(request):
    if request.method == "POST":
        query = request.POST["q"]
        entry = util.get_entry(query)

        if entry:
            url = reverse('entry', kwargs={'name': query})
            return HttpResponseRedirect(url)
        
        else:
            entries = util.list_entries()
            matches = []
            for entry in entries:
                if query.upper() in entry.upper():
                    matches.append(entry)
            if len(matches) == 0:
                return render(request, "encyclopedia/error.html", {
                    "message" : "There were no results for {search}".format(search=search)
                })
            else:
                return render(request, "encyclopedia/search.html", {
                    "entries" : matches
                })