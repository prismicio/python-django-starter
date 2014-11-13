import prismic
import views
from prismic import predicates
from django.conf import settings
from django.http import Http404


class PrismicHelper(object):

    def __init__(self, request, ref_id=None):
        self.api = prismic.get(
            settings.PRISMIC.get("api"), settings.PRISMIC.get("token"))
        self.link_resolver = views.link_resolver
        self.everything_form_name = "everything"
        self.google_id = self.api.experiments.current()
        cookie_ref = request.COOKIES.get(prismic.EXPERIMENTS_COOKIE)
        if ref_id is not None:
            self.ref = ref_id
        elif cookie_ref is not None:
            self.ref = cookie_ref
        else:
            self.ref = self.api.get_master()

    def form(self, name):
        form = self.api.form(name)
        form.ref(self.ref)
        return form

    def get_documents(self, document_ids, form_name="everything"):
        form = self.form(form_name)
        ids = ",".join(map(lambda i: "\"%s\"" % i, document_ids))
        form.query(predicates.any("document.id", ids))
        return form.submit().documents

    def get_document(self, document_id, form_name="everything"):
        form = self.form(form_name)
        form.query(predicates.at("document.id", document_id))
        document = form.submit().documents
        if document:
            return document[0]
        else:
            raise Http404

    def get_context(self):
        """Add context to the view dictionary"""
        return {"ref": self.ref, "link_resolver": self.link_resolver, "google_id": self.google_id}

    def get_bookmark(self, bookmark_id):
        bookmark = self.api.bookmarks[bookmark_id]
        return self.get_document(bookmark, self.everything_form_name)
