from django.shortcuts import render
from django.core.urlresolvers import reverse
from prismic_helper import PrismicHelper
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
    prismic = PrismicHelper()

    form = prismic.form("everything")
    documents = form.submit().documents

    parameters = {'documents': documents, 'context': prismic.get_context()}
    return render(request, 'prismic_app/index.html', parameters)


def detail(request, id, slug):
    prismic = PrismicHelper()

    document = prismic.get_document(id)

    parameters = {'context': prismic.get_context(), 'document': document}
    return render(request, 'prismic_app/detail.html', parameters)
