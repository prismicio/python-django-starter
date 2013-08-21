from django.http import HttpResponse, Http404
from django.conf import settings
from django.shortcuts import render, get_object_or_404
import prismic


def prismic_api():
    api = prismic.get(
        settings.PRISMIC.get("api"), settings.PRISMIC.get("token"))
    return api


def get_document(id):
    form = prismic_api().form("everything")
    form.ref("Master")
    form.query(r"""[[:d = at(document.id, "%s")]]""" % id)
    document = form.submit()
    if document:
        return document[0]
    else:
        raise Http404


def index(request):
    form = prismic_api().form("everything")
    form.ref("Master")
    documents = form.submit()
    return render(request, 'prismic_starter/index.html', {'documents': documents})


def detail(request, id, slug):
    document = get_document(id)
    return render(request, 'prismic_starter/detail.html', {'document': document})
