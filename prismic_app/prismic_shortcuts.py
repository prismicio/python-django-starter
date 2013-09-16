import prismic
import views
from django.conf import settings
from django.http import Http404
from django import template

class Prismic_Helper(object):

    def __init__(self, ref_id=None):
        self.api = prismic.get(
            settings.PRISMIC.get("api"), settings.PRISMIC.get("token"))
        self.link_resolver = views.link_resolver
        self.form_name = "everything"

        if ref_id != None:
            self.ref = ref_id
        else:
            self.ref = self.api.get_master().ref

    def form(self, name):
        form = self.api.form(name)
        form.ref(id=self.ref)
        return form

    def get_document(self, document_id):
        form = self.form(self.form_name)
        form.query(r"""[[:d = at(document.id, "%s")]]""" % document_id)
        document = form.submit()
        if document:
            return document[0]
        else:
            raise Http404

    def get_context(self):
        """Add context to the view dictionary"""
        return {"ref": self.ref, "link_resolver": self.link_resolver}


#template.add_to_builtins("prismic_shortcuts.as_html")

    # // -- Helper: Retrieve several documents by Id
    # def getDocuments(ids: String*)(implicit ctx: Prismic.Context): Future[Seq[Document]] = {
    #   ids match {
    #     case Nil => Future.successful(Nil)
    #     case ids => ctx.api.forms("everything").query(s"""[[:d = any(document.id, ${ids.mkString("[\"","\",\"","\"]")})]]""").ref(ctx.ref).submit()
    #   }
    # }

    # // -- Helper: Retrieve a single document from its bookmark
    # def getBookmark(bookmark: String)(implicit ctx: Prismic.Context): Future[Option[Document]] = {
    #   ctx.api.bookmarks.get(bookmark).map(id => getDocument(id)).getOrElse(Future.successful(None))
    # }
