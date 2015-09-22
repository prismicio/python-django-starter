import prismic
import views
from prismic import predicates
from django.conf import settings
from django.http import Http404


class PrismicHelper(object):

    def __init__(self, request):
        self.endpoint = settings.PRISMIC.get("api")
        self.api = prismic.get(self.endpoint, settings.PRISMIC.get("token"))
        self.link_resolver = views.link_resolver
        self.everything_form_name = "everything"
        self.google_id = self.api.experiments.current()
        preview_ref = request.COOKIES.get(prismic.PREVIEW_COOKIE)
        experiment_ref = self.api.experiments.ref_from_cookie(request.COOKIES.get(prismic.EXPERIMENTS_COOKIE))
        if preview_ref is not None:
            self.ref = preview_ref
        elif experiment_ref is not None:
            self.ref = experiment_ref
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
        return {
            "endpoint": self.endpoint,
            "ref": self.ref,
            "link_resolver": self.link_resolver,
            "google_id": self.google_id
        }

    def get_bookmark(self, bookmark_id):
        bookmark = self.api.bookmarks[bookmark_id]
        return self.get_document(bookmark, self.everything_form_name)
