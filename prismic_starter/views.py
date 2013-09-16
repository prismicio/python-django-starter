from django.http import HttpResponse, Http404
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from prismic_shortcuts import Prismic_Helper
import logging

logging.basicConfig(level=logging.DEBUG)

def link_resolver(document_link):
    """
    Creates a local link to document.

    document_link -- Fragment.DocumentLink object
    """

    #return reverse("prismic:document",args=document_link.id)
    return "/document/%s" % document_link.id

def index(request):
    prismic = Prismic_Helper()

    form = prismic.form("everything")
    documents = form.submit()
    parameters = {'documents': documents, 'context': prismic.get_context()}
    return render(request, 'prismic_starter/index.html', parameters)

def detail(request, id, slug):
    prismic = Prismic_Helper()

    document = prismic.get_document(id)
    parameters = {'document': document, 'context': prismic.get_context() }
    return render(request, 'prismic_starter/detail.html', parameters)