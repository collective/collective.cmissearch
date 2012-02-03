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

    def search(self, SearchableText):
        try:
            self.results = CMISZopeAPI(self.browser).search(SearchableText)
        except CMISConnectorError:
            logger.exception(
                "Error while search results for '%s'", SearchableText)
        return self.results

    def __len__(self):
        return len(self.results)

    def __iter__(self):
        return iter(self.results)
