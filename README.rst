=====================
collective.cmissearch
=====================

Presentation
============

collective.cmissearch is a Plone 3.2+ extension that let you search
into a `CMIS`_ document repository from Plone.

*This doesn't integrate the Plone search functionally with external
`CMIS`_ data*.  This provides a simple search form that does a search
both in Plone and in an `CMIS`_ repository.

This extension depends on `collective.cmisbrowser`. Each *CMIS
Browser* will indicate a starting point from which the searches will
be done.

Installation
============

Update buildout profile
-----------------------

Update your buildout profile to include the following eggs and zcml:

::

  eggs +=
      ...
      collective.cmisbrowser
      collective.cmissearch
  zcml +=
      ...
      collective.cmisbrowser
      collective.cmissearch

**Important:**

When using python 2.4.x you will also need to add *httpsproxy_urllib2*
as an egg.

Run the buildout
----------------

Run the buildout to reflect the changes you made to the profile.

::

  $ bin/buildout -v

Install the extension
---------------------

The extension can be installed through the ZMI or Plone control panel.

Through the ZMI
~~~~~~~~~~~~~~~

 - Go to the *portal quickinstaller* in the ZMI.

 - Check the extension *collective.cmissearch*.

 - Click the *install* button.

Through the *Plone control panel*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 - Go to *Site Setup*.

 - Choose *Add-on products*.

 - Check the extension *collective.cmissearch*.

 - Click the *Install* button.

Configuration
=============

 - Go to the desired *CMIS browser* of which you would like to set the
   search settings.

 - Click on the tab *Search Settings*

This will bring you to the *Edit Search settings* form with the
following parameters:

 - Activate search in this connector? Check this option to activate the search.

 - Priority of the search results (Required). Add a numeric value to set
   the priority. The higher the priority will be, the lower the result
   block will be displayed in the search results.

 - Activate CMIS-SCORE function to sort the results. Some CMIS server
   don't support this functionality. To be able to search content in
   such a server, you must deactivate this option.

 - Quote quote characters in the search terms. This option quotes the
   quote characters in the search terms. This is not defined by the CMIS
   norm but all CMIS server supports this functionality.

Adding a CMIS search portlet
============================

 - Go to *Manage portlets* in your Plone site were you would like to add
   a CMIS search portlet.

 - Select *CMIS Search portlet* from the list.

.. _CMIS: http://docs.oasis-open.org/cmis/CMIS/v1.0/cs01/cmis-spec-v1.0.html
