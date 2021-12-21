from django.http.response import HttpResponse
from django.shortcuts import render
from django.urls import reverse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def create(request):
    if request.method == "POST":
        if util.get_entry(request.POST[request.POST["name"]]):
            return render(request, "encyclopedia/error.html", {
                "message": "The page for {name} already exists, edit it instead if you believe it is wrong.".format(
                    name=request.POST["name"]
                )
            })
        util.save_entry(request.POST["name"], request.POST["entry"])
        url = reverse('entry', kwargs={'name': request.POST["name"]})
        return HttpResponse(url)

    def edit(request):
