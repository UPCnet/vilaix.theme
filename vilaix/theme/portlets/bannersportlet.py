# -*- coding: utf-8 -*-
from plone import api
from zope.interface import Interface

from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('genweb.banners')

from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from zope.component import getMultiAdapter
from genweb.banners.content import BannerContainer


class IBannersPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    # TODO: Add any zope.schema fields here to capture portlet configuration
    # information. Alternatively, if there are no settings, leave this as an
    # empty interface - see also notes around the add form and edit form
    # below.

    # some_field = schema.TextLine(title=_(u"Some field"),
    #                              description=_(u"A field to use"),
    #                              required=True)

    count = schema.Int(title=_(u'Number of banners to display'),
                       description=_(u'How many banners to list.'),
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
            source=SearchableTextSourceBinder({'type': BannerContainer},
                                              default_query='path:/material-multimedia/banners'))

class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IBannersPortlet)
    content = None

    # TODO: Set default values for the configurable parameters here

    # some_field = u""

    # TODO: Add keyword parameters for configurable parameters here
    # def __init__(self, some_field=u""):
    #    self.some_field = some_field

    def __init__(self, count=5, state=('published', ), content=None):
        self.count = count
        self.state = state
        self.content = content

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return _(u"Banners Portlet")


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('templates/bannersportlet.pt')

    def portal(self):
        return api.portal.get()

    def getBanners(self):
        return self._data()

    def _data(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        limit = self.data.count
        state = self.data.state
        content = self.data.content
        portal_state = getMultiAdapter((context, self.request),
            name='plone_portal_state')
        path = portal_state.navigation_root_path()
        return catalog(portal_type='Banner',
                       review_state=state,
                       path=path + content,
                       sort_on='getObjPositionInParent',
                       sort_limit=limit)[:limit]

    def test(self, value, trueVal, falseVal):
        """
            helper method, mainly for setting html attributes.
        """
        if value:
            return trueVal
        else:
            return falseVal


    def getAltAndTitle(self, altortitle):
        """ Funcio que extreu idioma actiu i afegeix al alt i al title de les imatges del banner
            el literal Obriu l'enllac en una finestra nova.
        """
        return '%s, %s' % (altortitle.decode('utf-8'),
            self.portal().translate(_('obrir_link_finestra_nova', default=u"(obriu en una finestra nova)")))


    # def getAltAndTitle(self, altortitle):
    #     """Funcio que extreu idioma actiu i afegeix al alt i al title de les imatges del banner
    #        el literal Obriu l'enllac en una finestra nova
    #     """
    #     lt = getToolByName(self, 'portal_languages')
    #     idioma = lt.getPreferredLanguage()
    #     str = ''
    #     if idioma == 'ca':
    #         str = "(obriu en una finestra nova)"
    #     if idioma == 'es':
    #         str = "(abre en ventana nueva)"
    #     if idioma == 'en':
    #         str = "(open in new window)"
    #     if str == '':
    #         str = "(obriu en una finestra nova)"
    #     return altortitle + ', ' + str


# NOTE: If this portlet does not have any configurable parameters, you can
# inherit from NullAddForm and remove the form_fields variable.


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IBannersPortlet)
    label = _(u"Add banners portlet")
    description = _(u"This portlet displays the site banners.")
    form_fields['content'].custom_widget = UberSelectionWidget

    def create(self, data):
        return Assignment(count=data.get('count', 5), state=data.get('state', ('published',)), content=data.get('content', True))


# NOTE: IF this portlet does not have any configurable parameters, you can
# remove this class definition and delete the editview attribute from the
# <plone:portlet /> registration in configure.zcml

class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IBannersPortlet)
    label = _(u"Edit banners portlet")
    description = _(u"This portlet displays the site banners.")
    form_fields['content'].custom_widget = UberSelectionWidget
