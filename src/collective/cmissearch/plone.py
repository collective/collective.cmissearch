# -*- coding: utf-8 -*-
# Copyright (c) 2011 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from zope.interface import implements
from zope.i18nmessageid import MessageFactory

from collective.cmissearch.interfaces import ISearchSource

_ = MessageFactory('collective.cmissearch')


class PloneSearchSource(object):
    implements(ISearchSource)

    label = _("Search in Plone")
    priority = 0

    def __init__(self, context):
        self.catalog = context.catalog
        self.results = []

    def search(self, SearchableText):
        return self.catalog(SearchableText=SearchableText)

    def __len__(self):
        return len(self.results)

    def __iter__(self):
        return iter(self.results)

