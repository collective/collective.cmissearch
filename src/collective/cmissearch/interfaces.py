# -*- coding: utf-8 -*-
# Copyright (c) 2011 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id$

from zope.interface import Interface, Attribute


class ISearchSource(Interface):
    label = Attribute(u"Source label")
    priority = Attribute(u"Display priority")

    def search(SearchableText):
        """Search for SearchableText in content.
        """

    def __len__():
        """Return the number of results.
        """

    def __iter__():
        """Iter on the results.
        """


class ISearchContext(Interface):
    catalog = Attribute(u"Plone catalog")

    def sources():
        """Return all sources candidates.
        """
