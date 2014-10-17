# -*- coding: utf-8 -*-
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.layout.navigation.root import getNavigationRootObject
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements
from zope import schema

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.portlets import PloneMessageFactory as _
from plone.app.portlets.cache import render_cachekey
from plone.app.portlets.portlets import base
from plone.app.contenttypes.interfaces import INewsItem

from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget


class ISeccioPortlet(IPortletDataProvider):

    name = schema.TextLine(
            title=_(u"label_navigation_title", default=u"Title"),
            description=_(u"help_navigation_title",
                          default=u"The title of the navigation tree."),
            default=u"",
            required=False)

    count = schema.Int(title=_(u'Number of items to display'),
                       description=_(u'How many items to list.'),
                       required=True,
                       default=5)

    state = schema.Tuple(title=_(u"Workflow state"),
                         description=_(u"Items in which workflow state to show."),
                         default=('published', ),
                         required=True,
                         value_type=schema.Choice(
                             vocabulary="plone.app.vocabularies.WorkflowStates")
                         )

    content = schema.Choice(
            title=_(u"label_navigation_root_path", default=u"Root node"),
            description=_(u'help_navigation_root',
                          default=u"You may search for and choose a folder "
                                    "to act as the root of the navigation tree. "
                                    "Leave blank to use the Plone site root."),
            required=False,
            source=SearchableTextSourceBinder({'portal_type': 'Folder' },
                                              default_query='path:'))

class Assignment(base.Assignment):
    implements(ISeccioPortlet)

    def __init__(self, name="", count=5, state=('published', ), content=None):
        self.name = name
        self.count = count
        self.state = state
        self.content = content

    @property
    def title(self):
        """
        Display the name in portlet mngmt interface
        """
        if self.name:
            return self.name
        return _(u'Seccio')


class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('templates/seccio.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

    @ram.cache(render_cachekey)
    def render(self):
        return xhtml_compress(self._template())

    @property
    def available(self):
        return self.data.count > 0 and len(self._data())

    def published_news_items(self):
        return self._data()

    def all_news_link(self):
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request),
            name='plone_portal_state')
        portal = portal_state.portal()
        if 'news' in getNavigationRootObject(context, portal).objectIds():
            return '%s/news' % portal_state.navigation_root_url()
        return None


    def abrevia(self, summary, sumlenght):
        """ Retalla contingut de cadenes
        """
        i=0
        bb=''

        if sumlenght<len(summary):
            bb=summary[:sumlenght]

            lastspace = bb.rfind(' ')
            cutter = lastspace
            precut = bb[0:cutter]

            if precut.count('<b>')>precut.count('</b>'):
                cutter = summary.find('</b>',lastspace)+4
            bb=summary[0:cutter]

            if bb.count('<p')>precut.count('</p'):
                bb+='...</p>'
            else:
                bb=bb+'...'
        else:
            bb=summary

        return bb

    def getTitol(self):
        return self.data.name

    # def getFolderNoticies(self):
    #     noticies = self._data()
    #     for a in noticies:
    #        new = a.getObject()
    #     return new.__parent__.title

    def dadesNoticies(self):
        noticies = self._data()
        dades = [dict(id=a.id,
                     text =self.abrevia(a.getObject().text.raw,100),
                     url=a.getURL(),
                     title=a.Title,
                     new = a.getObject(),
                     date = str(a.getObject().effective_date.day()) + '/' + str(a.getObject().effective_date.month()) + '/' + str(a.getObject().effective_date.year()),
                     image = a.getObject().image) for a in noticies]
        return dades

    @memoize
    def _data(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        portal_state = getMultiAdapter((context, self.request),
            name='plone_portal_state')
        path = portal_state.navigation_root_path() + self.data.content
        limit = self.data.count
        state = self.data.state
        return catalog(portal_type='News Item',
                       review_state=state,
                       path=path,
                       destacat = False,
                       sort_on='Date',
                       sort_order='reverse',
                       sort_limit=limit)[:limit]

class AddForm(base.AddForm):
    form_fields = form.Fields(ISeccioPortlet)
    label = _(u"Add Seccio News Portlet")
    description = _(u"This portlet displays News Items of section.")
    form_fields['content'].custom_widget = UberSelectionWidget

    def create(self, data):
        return Assignment(name=data.get('name', ""), count=data.get('count', 5), state=data.get('state', ('published', )), content=data.get('content', True))



class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(ISeccioPortlet)
    label = _(u"Edit Seccio News Portlet")
    description = _(u"This portlet displays News Items of section.")
    form_fields['content'].custom_widget = UberSelectionWidget
