
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.cachedescriptors.property import CachedProperty

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ISearchPortlet(IPortletDataProvider):
    pass


class SearchPortlet(base.Assignment):
    implements(ISearchPortlet)


class SearchPortletRenderer(base.Renderer):
    render = ViewPageTemplateFile('templates/searchportlet.pt')
    __allow_access_to_unprotected_subobjects__ = 1

    def get_browser(self):
       try:
            return self.context.getCMISBrowser()
       except:
            return None

    @CachedProperty
    def browser_url(self):
        browser = self.get_browser()
        if browser is not None:
            return browser.absolute_url()
        return None

    @CachedProperty
    def browser_title(self):
        browser = self.get_browser()
        if browser is not None:
            return browser.Title()
        return None



class SearchPortletAddForm(base.NullAddForm):

    def create(self):
        return SearchPortlet()
