# -*- coding: utf-8 -*-
# Copyright (c) 2011 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

import operator

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

from zope.interface import implements

from collective.cmissearch.interfaces import ISearchSource, ISearchContext


class SearchPage(BrowserView):
    implements(ISearchContext)

    def candidates(self):
        yield self
        for browser in self.catalog(meta_type=['CMIS Browser']):
            yield browser.getObject()

    def search(self, SearchableText):
        for candidate in self.candidates():
            source = ISearchSource(candidate, None)
            if source is not None:
                source.search(SearchableText)
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
