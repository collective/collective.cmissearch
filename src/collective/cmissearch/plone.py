# -*- coding: utf-8 -*-
# Copyright (c) 2011 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from zope.interface import implements
from zope.i18nmessageid import MessageFactory

from collective.cmissearch.interfaces import ISearchSource
from Products.CMFCore.utils import getToolByName

_ = MessageFactory('collective.cmissearch')


class PloneSearchSource(object):
    implements(ISearchSource)
    priority = 0

    @property
    def label(self):
        return _("Search in ${site}",
                 mapping={'site': self.site.Title()})

    def __init__(self, context):
        self.catalog = context.catalog
        self.site = getToolByName(context.context, 'portal_url').getPortalObject()
        self.results = []

    def search(self, SearchableText):
        self.results = self.catalog(SearchableText=SearchableText)
        return self.results

    def __len__(self):
        return len(self.results)

    def __iter__(self):
        return (r.getObject() for r in self.results)

