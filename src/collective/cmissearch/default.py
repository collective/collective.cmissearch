# -*- coding: utf-8 -*-
# Copyright (c) 2011 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from zope.interface import implements
from zope.i18nmessageid import MessageFactory

from collective.cmissearch.interfaces import ISearchSource
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.PloneBatch import Batch

_ = MessageFactory('collective.cmissearch')


class PloneSearchSource(object):
    implements(ISearchSource)
    priority = 0
    available = True

    @property
    def label(self):
        return _("Search in ${site}",
                 mapping={'site': self.site.Title()})

    def __init__(self, context):
        self.catalog = context.catalog
        self.site = getToolByName(context.context, 'portal_url').getPortalObject()
        self.results = []
        self.batch = []
        self.batch_key = 'b_start'
        self.batch_size = None

    def search(self, SearchableText, batch_position=None, batch_size=10):
        self.results = self.catalog(SearchableText=SearchableText)
        if batch_position is not None:
            self.batch_size = batch_size
            self.batch = Batch(self.results, batch_size, batch_position, b_start_str=self.batch_key)
        else:
            self.batch = self.results
        return self.results

    def __len__(self):
        return len(self.results)

    def __iter__(self):
        return (r.getObject() for r in self.batch)

