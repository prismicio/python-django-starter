import prismic
import views
from django.conf import settings
from django.http import Http404
from django import template

class PrismicHelper(object):

    def __init__(self, ref_id=None):
        self.api = prismic.get(
            settings.PRISMIC.get("api"), settings.PRISMIC.get("token"))
        self.link_resolver = views.link_resolver
        self.everything_form_name = "everything"

        if ref_id != None:
            self.ref = ref_id
        else:
            self.ref = self.api.get_master()

    def form(self, name):
        form = self.api.form(name)
        form.ref(id=self.ref)
        return form

    def get_document(self, document_id, form_name="everything"):
        form = self.form(form_name)
        form.query(r"""[[:d = at(document.id, "%s")]]""" % document_id)
        document = form.submit()
        if document:
            return document[0]
        else:
            raise Http404

    def get_context(self):
        """Add context to the view dictionary"""
        return {"ref": self.ref, "link_resolver": self.link_resolver}

    def get_bookmark(self, bookmark_id):
        bookmark = self.api.bookmarks[bookmark_id]
        return self.get_document(bookmark, self.everything_form_name)