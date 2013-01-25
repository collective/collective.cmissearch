# Copyright (c) 2012 Vlaamse Overheid. All rights reserved.
# See also LICENSE.txt

import operator

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.PloneBatch import Batch

from zope.interface import implements

from collective.cmissearch.interfaces import ISearchSource, ISearchContext
from collective.cmissearch.interfaces import ICMISSearchConfiguration
from collective.cmisbrowser.cmis.api import CMISZopeAPI
from collective.cmisbrowser.interfaces import ICMISBrowser


class SearchPage(BrowserView):
    implements(ISearchContext)

    batch_size = 10

    def candidates(self):
        yield self
        for brain in self.catalog(meta_type=['CMIS Browser']):
            browser = brain.getObject()
            yield browser

    def search(self, SearchableText):
        for candidate in self.candidates():
            source = ISearchSource(candidate, None)
            if source is not None and source.available:
                batch_position = self.request.get(source.batch_key, 0)
                try:
                    batch_position = int(batch_position)
                except (ValueError, TypeError):
                    batch_position = 0
                source.search(SearchableText, batch_position, self.batch_size)
                yield source

    def update(self):
        self.is_searching = 'SearchableText' in self.request.form
        self.results = []
        self.count = 0
        if self.is_searching:
            self.catalog = getToolByName(self.context, 'portal_catalog')
            self.results.extend(self.search(self.request['SearchableText']))
            self.results.sort(key=operator.attrgetter('priority'))
            self.count = reduce(operator.add, [0] + map(len, self.results))

    def __call__(self):
        self.update()
        return self.index()
        
        
class SimpleSearchPage(BrowserView):
    batch_size = 25

    def update(self):
        self.is_searching = 'SearchableText' in self.request.form
        self.results = []
        self.count = 0
        if self.is_searching:
            try:
                browser = self.context.getCMISBrowser()
            except:
                return
            if not ICMISBrowser.providedBy(browser):
                return
            text = self.request.form['SearchableText']
            settings = ICMISSearchConfiguration(browser)
            api = CMISZopeAPI(browser)
            batch_start = self.request.form.get('b_start', '0')
            try:
                batch_start = int(batch_start)
            except:
                batch_start = 0
            self.results = api.search(
                text, quotable=settings.quote, scorable=settings.score)
            self.count = len(self.results)
            self.batch = Batch(self.results, self.batch_size, batch_start)

    def __call__(self):
        self.update()
        return self.index() 
