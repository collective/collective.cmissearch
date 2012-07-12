# -*- coding: utf-8 -*-
# Copyright (c) 2011 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

import logging

from zope.interface import implements
from zope.i18nmessageid import MessageFactory

from collective.cmissearch.interfaces import ISearchSource
from collective.cmisbrowser.cmis.api import CMISZopeAPI
from collective.cmisbrowser.errors import CMISConnectorError

from Products.CMFPlone.PloneBatch import Batch

_ = MessageFactory('collective.cmissearch')
logger = logging.getLogger('collective.cmissearch')


class CMISSearchSource(object):
    implements(ISearchSource)

    @property
    def label(self):
        return _(u"Search in ${domain}", mapping={'domain': self.browser.Title()})

    priority = 10

    def __init__(self, browser):
        self.browser = browser
        self.results = []
        self.batch = []
        self.batch_key = 'b_' + browser.getId()
        self.batch_size = None

    def search(self, SearchableText, batch_position=None, batch_size=10):
        try:
            self.results = CMISZopeAPI(self.browser).search(SearchableText)
        except CMISConnectorError:
            logger.exception(
                "Error while search results for '%s'", SearchableText)
        if batch_position is not None:
            self.batch_size = batch_size
            self.batch = Batch(self.results, batch_size, batch_position, b_start_str=self.batch_key)
        else:
            self.batch = self.results
        return self.results

    def __len__(self):
        return len(self.results)

    def __iter__(self):
        return iter(self.batch)
