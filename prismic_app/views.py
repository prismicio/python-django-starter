from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import Http404

from prismic_helper import PrismicHelper
from prismic import PREVIEW_COOKIE

#import logging

#logging.basicConfig(level=logging.DEBUG)
#log = logging.getLogger(__name__)

def link_resolver(document_link):
    """
    Creates a local link to document.

    document_link -- Fragment.DocumentLink object
    """

    return reverse('prismic:document', kwargs={'id': document_link.get_document_id(), 'slug': document_link.get_document_slug()})


def index(request):
    prismic = PrismicHelper(request)

    form = prismic.form("everything")
    documents = form.submit().documents

    parameters = {'documents': documents, 'context': prismic.get_context()}
    return render(request, 'prismic_app/index.html', parameters)


def detail(request, id, slug):
    prismic = PrismicHelper(request)

    document = prismic.get_document(id)

    parameters = {'context': prismic.get_context(), 'document': document}
    return render(request, 'prismic_app/detail.html', parameters)


def preview(request):
    prismic = PrismicHelper(request)

    token = request.GET.get('token')

    if token is None:
        raise Http404

    url = prismic.api.preview_session(token, prismic.link_resolver, '/')

    response = redirect(url)
    response.set_cookie(PREVIEW_COOKIE, token, max_age=1800, httponly=False)
    return response
