# -*- coding: utf-8 -*-
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from plone.app.layout.navigation.defaultpage import isDefaultPage
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.layout.navigation.interfaces import INavigationQueryBuilder
from plone.app.layout.navigation.navtree import buildFolderTree
from plone.app.layout.navigation.root import getNavigationRoot
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from zope.component import adapts, getMultiAdapter, queryUtility
from zExceptions import NotFound
from zope.formlib import form
from zope.interface import implements, Interface
from zope import schema

from Acquisition import aq_inner, aq_base, aq_parent
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFDynamicViewFTI.interface import IBrowserDefault
from Products.CMFPlone import utils
from Products.CMFPlone.browser.navtree import SitemapNavtreeStrategy
from Products.CMFPlone.interfaces import INonStructuralFolder
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.portlets import PloneMessageFactory as _
from plone.app.portlets.portlets import base


class INavigationFixedPortlet(IPortletDataProvider):
    """A portlet which can render the navigation tree
    """

    name = schema.TextLine(
            title=_(u"label_navigation_title", default=u"Title"),
            description=_(u"help_navigation_title",
                          default=u"The title of the navigation tree."),
            default=u"",
            required=False)

    root = schema.Choice(
            title=_(u"label_navigation_root_path", default=u"Root node"),
            description=_(u'help_navigation_root',
                          default=u"You may search for and choose a folder "
                                    "to act as the root of the navigation tree. "
                                    "Leave blank to use the Plone site root."),
            required=False,
            source=SearchableTextSourceBinder({'is_folderish': True},
                                              default_query='path:'))

    
    currentFolderOnly = schema.Bool(
            title=_(u"label_current_folder_only",
                    default=u"Only show the contents of the current folder."),
            description=_(u"help_current_folder_only",
                          default=u"If selected, the navigation tree will "
                                   "only show the current folder and its "
                                   "children at all times."),
            default=False,
            required=False)

    # topLevel = schema.Int(
    #         title=_(u"label_navigation_startlevel", default=u"Start level"),
    #         description=_(u"help_navigation_start_level",
    #             default=u"An integer value that specifies the number of folder "
    #                      "levels below the site root that must be exceeded "
    #                      "before the navigation tree will display. 0 means "
    #                      "that the navigation tree should be displayed "
    #                      "everywhere including pages in the root of the site. "
    #                      "1 means the tree only shows up inside folders "
    #                      "located in the root and downwards, never showing "
    #                      "at the top level."),
    #         default=0,
    #         required=False)

    # bottomLevel = schema.Int(
    #         title=_(u"label_navigation_tree_depth",
    #                 default=u"Navigation tree depth"),
    #         description=_(u"help_navigation_tree_depth",
    #                       default=u"How many folders should be included "
    #                                "before the navigation tree stops. 0 "
    #                                "means no limit. 1 only includes the "
    #                                "root folder."),
    #         default=3,
    #         required=False)


class Assignment(base.Assignment):
    implements(INavigationFixedPortlet)

    name = ""
    root = None
    currentFolderOnly = False    
    # topLevel = 0
    #bottomLevel = 3

    def __init__(self, name="", root=None, currentFolderOnly=False):
        self.name = name
        self.root = root
        self.currentFolderOnly = currentFolderOnly       
        # self.topLevel = topLevel
        #self.bottomLevel = bottomLevel

    @property
    def title(self):
        """
        Display the name in portlet mngmt interface
        """
        if self.name:
            return self.name
        return _(u'Navigation Fixed')


class Renderer(base.Renderer):

    def __init__(self, context, request, view, manager, data):
        base.Renderer.__init__(self, context, request, view, manager, data)

        self.properties = getToolByName(context, 'portal_properties').navtree_properties
        self.urltool = getToolByName(context, 'portal_url')

    render = ViewPageTemplateFile('templates/navigationfixed.pt') 

    def mostrarFillsCarpeta(self, carpeta):
        """ Busca etiquetes dintre del portal_vocabulary segons idioma
        """       
        rootpath = self.getNavRootPath() + '/' +  carpeta.id
        resultats = []
       
        carpetes = self.context.portal_catalog.searchResults(portal_type='Folder',
                                                             path={'query':rootpath, 'depth':1,},
                                                             sort_on='getObjPositionInParent',
                                                             review_state = 'published')
        for valor in carpetes:
            obj = valor.getObject()
            url = obj.absolute_url()
            collapse = '#' + obj.id
            resultats.append({'id': obj.id, 'title': obj.title, 'url': url, 'collapse': collapse })

        return resultats     
    
    def mostrarCarpetes(self):
        """ Busca etiquetes dintre del portal_vocabulary segons idioma
        """       
        rootpath = self.getNavRootPath()
        resultats = []
        
        carpetes = self.context.portal_catalog.searchResults(portal_type='Folder',
                                                             path={'query':rootpath, 'depth':1,},
                                                             sort_on='getObjPositionInParent',
                                                             review_state = 'published')
        for valor in carpetes:
            obj = valor.getObject()
            url = obj.absolute_url()
            collapse = '#' + obj.id
            fills = self.mostrarFillsCarpeta(obj)
            resultats.append({'id': obj.id, 'title': obj.title, 'url': url, 'collapse': collapse, 'fills': fills })

        return resultats   
           
    @memoize
    def getNavRootPath(self):
        currentFolderOnly = self.data.currentFolderOnly or \
                            self.properties.getProperty('currentFolderOnlyInNavtree', False)
        #topLevel = self.data.topLevel or self.properties.getProperty('topLevel', 0)
        return getRootPath(self.context, currentFolderOnly, self.data.root)

def getRootPath(context, currentFolderOnly, root):
    """Helper function to calculate the real root path
    """
    context = aq_inner(context)
    if currentFolderOnly:
        folderish = getattr(aq_base(context), 'isPrincipiaFolderish', False) and \
                    not INonStructuralFolder.providedBy(context)
        parent = aq_parent(context)

        is_default_page = False
        browser_default = IBrowserDefault(parent, None)
        if browser_default is not None:
            is_default_page = (browser_default.getDefaultPage() == context.getId())

        if not folderish or is_default_page:
            return '/'.join(parent.getPhysicalPath())
        else:
            return '/'.join(context.getPhysicalPath())

    rootPath = getNavigationRoot(context, relativeRoot=root)

    # Adjust for topLevel
    # if topLevel > 0:
    #     contextPath = '/'.join(context.getPhysicalPath())
    #     if not contextPath.startswith(rootPath):
    #         return None
    #     contextSubPathElements = contextPath[len(rootPath) + 1:]
    #     if contextSubPathElements:
    #         contextSubPathElements = contextSubPathElements.split('/')
    #         if len(contextSubPathElements) < topLevel:
    #             return None
    #         rootPath = rootPath + '/' + '/'.join(contextSubPathElements[:topLevel])
    #     else:
    #         return None

    return rootPath

    
class AddForm(base.AddForm):
    form_fields = form.Fields(INavigationFixedPortlet)
    form_fields['root'].custom_widget = UberSelectionWidget
    label = _(u"Add Navigation Portlet")
    description = _(u"This portlet displays a navigation tree.")

    def create(self, data):
        return Assignment(name=data.get('name', ""),
                          root=data.get('root', ""))


class EditForm(base.EditForm):
    form_fields = form.Fields(INavigationFixedPortlet)
    form_fields['root'].custom_widget = UberSelectionWidget
    label = _(u"Edit Navigation Portlet")
    description = _(u"This portlet displays a navigation tree.")


