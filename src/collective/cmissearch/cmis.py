# -*- coding: utf-8 -*-
# Copyright (c) 2011 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

import logging

from zope.annotation import IAnnotations
from zope.component import adapts
from zope.i18nmessageid import MessageFactory
from zope.interface import implements
from zope.formlib.form import Fields

from plone.app.form.base import EditForm

from collective.cmisbrowser.cmis.api import CMISZopeAPI
from collective.cmisbrowser.errors import CMISConnectorError
from collective.cmisbrowser.interfaces import ICMISBrowser
from collective.cmissearch.interfaces import ICMISSearchConfiguration
from collective.cmissearch.interfaces import ISearchSource

from Products.CMFPlone.PloneBatch import Batch

_ = MessageFactory('collective.cmissearch')
logger = logging.getLogger('collective.cmissearch')


class CMISSearchSource(object):
    implements(ISearchSource)
    adapts(ICMISBrowser)

    def __init__(self, browser):
        self.browser = browser
        self.settings = ICMISSearchConfiguration(browser)
        self.results = []
        self.batch = []
        self.batch_key = 'b_' + browser.getId()
        self.batch_size = None

    @property
    def label(self):
        return _(u"Search in ${domain}", mapping={'domain': self.browser.Title()})

    @property
    def priority(self):
        return self.settings.priority

    @property
    def available(self):
        return self.settings.activated

    def search(self, SearchableText, batch_position=None, batch_size=10):
        try:
            self.results = CMISZopeAPI(self.browser).search(
                SearchableText,
                quotable=self.settings.quote,
                scorable=self.settings.score)
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


def annotations(key, default):

    def setter(self, value):
        self.annotations[key] = value

    def getter(self):
        return self.annotations.get(key, default)

    return property(getter, setter)


class CMISSearchConfiguration(object):
    adapts(ICMISBrowser)
    implements(ICMISSearchConfiguration)

    def __init__(self, context):
        self.context = context
        self.annotations = IAnnotations(context)

    activated = annotations('collective.cmissearch.activated', True)
    priority = annotations('collective.cmissearch.priority', 10)
    score = annotations('collective.cmissearch.score', True)
    quote = annotations('collective.cmissearch.quote', False)


class CMISEditSearchSettings(EditForm):
    label = _(u"Edit Search settings")
    description = _(u"Configure search related settings.")
    form_fields = Fields(ICMISSearchConfiguration)
