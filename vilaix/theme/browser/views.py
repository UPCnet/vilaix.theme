# -*- coding: utf-8 -*-
from five import grok
from zope.interface import alsoProvides
from Acquisition import aq_inner
from zope.interface import Interface
from zope.component import getMultiAdapter, queryMultiAdapter, getUtility, queryUtility
from zope.contentprovider import interfaces

from Products.CMFPlone import utils
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.browser.navigation import CatalogNavigationTabs
from Products.CMFPlone.browser.navigation import get_id, get_view_url

from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletManagerRenderer
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from plone.portlets.constants import CONTEXT_CATEGORY
from plone.memoize import ram

from genweb.core.interfaces import IGenwebLayer, IHomePage
from genweb.theme.browser.interfaces import IGenwebTheme, IHomePageView
from genweb.theme.browser.views import HomePageBase
from genweb.core.utils import genweb_config, pref_lang
from genweb.portlets.browser.manager import ISpanStorage

from scss import Scss

from plone.formwidget.recaptcha.view import RecaptchaView, IRecaptchaInfo
from recaptcha.client.captcha import displayhtml

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from interfaces import IVilaixTheme
from plone.app.collection.interfaces import ICollection
from vilaix.theme.portlets.utils import setupQueryPortlet, setPortletAssignment, setupNavPortlet
from vilaix.theme.portlets.queryportlet import Assignment as QueryPortletAssignment
from plone.app.portlets.portlets.navigation import Assignment as NavPortletAssignment


class IInitializedPortlets(Interface):
    """
    Marker interface to mark wether the default portlets have been initialized
    """


class CollectionPortletView(HomePageBase):
    grok.implements(IHomePageView)
    grok.context(ICollection)
    grok.layer(IVilaixTheme)
    grok.name('subhome')

    def setDefaultPortlets(self):
        """
        """

        # Portlet slider

        assignment = setPortletAssignment(3, self.context, 'slider', QueryPortletAssignment, span=7)
        query = [{u'i': u'portal_type', u'o': u'plone.app.querystring.operation.selection.is', u'v': [u'Slider']}]
        setupQueryPortlet(assignment, u'SLIDER', query, None, False, u"")

        # Portlet Tramit

        assignment = setPortletAssignment(3, self.context, 'tramits', QueryPortletAssignment, span=7)
        query = [{u'i': u'portal_type', u'o': u'plone.app.querystring.operation.selection.is', u'v': [u'Tramit']}]
        setupQueryPortlet(assignment, u'TRAMITS', query, 3, False, u"")

        # Portlet Directori

        assignment = setPortletAssignment(6, self.context, 'directori', QueryPortletAssignment, span=5)
        query = [{u'i': u'portal_type', u'o': u'plone.app.querystring.operation.selection.is', u'v': [u'Equipament']}]
        setupQueryPortlet(assignment, u'DIRECTORI', query, None, False, u"")

        # Portlet Noticies

        assignment = setPortletAssignment(7, self.context, 'noticies', QueryPortletAssignment, span=7)
        query = [{u'i': u'portal_type', u'o': u'plone.app.querystring.operation.selection.is', u'v': [u'News Item']}]
        setupQueryPortlet(assignment, u'NOTÍCIES', query, 2, False, u"")

        # Portlet Agenda

        assignment = setPortletAssignment(10, self.context, 'agenda', QueryPortletAssignment, span=5)
        query = [{u'i': u'portal_type', u'o': u'plone.app.querystring.operation.selection.is', u'v': [u'Event']},
                 {u'i': u'end', u'o': u'plone.app.querystring.operation.date.afterToday'}]

        setupQueryPortlet(assignment, u'AGENDA', query, 3, False, u"")

        # Portlet navegacio
        assignment = setPortletAssignment(1, self.context, 'navegacio', NavPortletAssignment)
        setupNavPortlet(assignment, u'NAVEGACIÓ', 3)

        # Portlet Plans i Campanyes

        assignment = setPortletAssignment(1, self.context, 'plans', QueryPortletAssignment)
        query = [{u'i': u'portal_type', u'o': u'plone.app.querystring.operation.selection.is', u'v': [u'Banner']}]
        setupQueryPortlet(assignment, u'PLANS I CAMPANYES', query, 4, False, u"")

        # Portlet Arxius relacionats

        assignment = setPortletAssignment(1, self.context, 'arxius', QueryPortletAssignment)
        query = [{u'i': u'portal_type', u'o': u'plone.app.querystring.operation.selection.is', u'v': [u'File']}]
        setupQueryPortlet(assignment, u'ARXIUS RELACIONATS', query, None, False, u"")

        # No heredar mai dels pares
        for i in range(1, 11):
            portlet_manager_name = u'genweb.portlets.HomePortletManager{}'.format(i)
            obj = self.context
            portlet_manager = queryUtility(IPortletManager, name=portlet_manager_name)
            blacklist = getMultiAdapter((obj, portlet_manager), ILocalPortletAssignmentManager)
            blacklist.setBlacklistStatus(CONTEXT_CATEGORY, True)

        alsoProvides(self.context, IInitializedPortlets)

    def render(self):
        template = ViewPageTemplateFile('views_templates/subhome.pt')
        if not IInitializedPortlets.providedBy(self.context) or self.request.get('reset', None):
            self.setDefaultPortlets()
        return template(self)


class GWConfig(grok.View):
    grok.context(Interface)

    def render(self):
        return genweb_config()


class homePage(grok.View):
    """ This is the special view for the homepage containing support for the
        portlet managers provided by the package genweb.portlets.
        It's restrained to IGenwebTheme layer to prevent it will interfere with
        the one defined in the Genweb legacy theme (v4).
    """
    grok.implements(IHomePageView)
    grok.context(IPloneSiteRoot)
    grok.layer(IVilaixTheme)

    def update(self):
        self.portlet_container = self.getPortletContainer()

    def getPortletContainer(self):
        context = aq_inner(self.context)
        pc = getToolByName(context, 'portal_catalog')
        result = pc.searchResults(object_provides=IHomePage.__identifier__,
                                  Language=pref_lang())
        if result:
            # Return the object without forcing a getObject()
            return getattr(context, result[0].id, context)
        else:
            # If this happens, it's bad. Implemented as a fallback
            return context

    def renderProviderByName(self, provider_name):
        provider = queryMultiAdapter(
            (self.portlet_container, self.request, self),
            interfaces.IContentProvider, provider_name)

        provider.update()

        return provider.render()

    def getSpanValueForManager(self, manager):
        portletManager = getUtility(IPortletManager, manager)
        spanstorage = getMultiAdapter((self.portlet_container, portletManager), ISpanStorage)
        span = spanstorage.span
        if span:
            return span
        else:
            return '4'

    def have_portlets(self, manager_name, view=None):
        """Determine whether a column should be shown. The left column is called
        plone.leftcolumn; the right column is called plone.rightcolumn.
        """
        force_disable = self.request.get('disable_' + manager_name, None)
        if force_disable is not None:
            return not bool(force_disable)

        context = self.portlet_container
        if view is None:
            view = self

        manager = queryUtility(IPortletManager, name=manager_name)
        if manager is None:
            return False

        renderer = queryMultiAdapter((context, self.request, view, manager), IPortletManagerRenderer)
        if renderer is None:
            renderer = getMultiAdapter((context, self.request, self, manager), IPortletManagerRenderer)

        return renderer.visible
