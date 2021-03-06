# Copyright (c) 2013 Beleidsdomein Leefmilieu, Natuur en Energie (LNE) and Vlaamse Milieumaatschappij (VMM). All rights reserved.
# See also LICENSE.txt

from zope import schema
from zope.interface import Interface, Attribute
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('collective.cmissearch')


class ICMISSearchConfiguration(Interface):
    """Configuration parameters for a CMISBrowser.
    """
    activated = schema.Bool(
        title=_(u"Activate search in this connector?"),
        default=True,
        required=True)
    priority = schema.Int(
        title=_(u"Priority of the search results"),
        description=_(u"Higher the priority will be, lower the result block "
                      u"will be displayed in the search results."),
        required=True,
        default=10,
        min=1)
    score = schema.Bool(
        title=_(u"Activate CMIS-SCORE function to sort the results"),
        description=_(u"Some CMIS server doesn't support this functionality. "
                      u"To be able to search content in such server, you must "
                      u"desactivate this option."),
        default=True,
        required=True)
    quote = schema.Bool(
        title=_(u"Quote quote characters in the search terms"),
        description=_(u"Quote the quote characters in the search terms. "
                      u"This is not defined by the CMIS norm, and all CMIS server "
                      u"supports this functionality."),
        default=False,
        required=True)


class ISearchSource(Interface):
    """Search backend in the search form.

    Current implementations are to search within Plone and
    CMISBrowser.
    """
    label = Attribute(u"Source label")
    priority = Attribute(u"Display priority")
    available = Attribute(u"Boolean indicating if the source is available")

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
    """Context passed to ISearchSource.
    """
    catalog = Attribute(u"Plone catalog")

    def sources():
        """Return all sources candidates.
        """
