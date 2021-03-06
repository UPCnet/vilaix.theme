# -*- coding: utf-8 -*-
import re
from five import grok
from cgi import escape
from Acquisition import aq_inner
from AccessControl import getSecurityManager
from zope.interface import Interface
from zope.component import getMultiAdapter
from zope.component.hooks import getSite

from plone.memoize.view import memoize_contextless

from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.layout.viewlets.common import PersonalBarViewlet, GlobalSectionsViewlet, PathBarViewlet
from plone.app.layout.viewlets.common import SearchBoxViewlet, TitleViewlet, ManagePortletsFallbackViewlet
from plone.app.layout.viewlets.interfaces import IHtmlHead, IPortalTop, IPortalHeader, IBelowContent
from plone.app.layout.viewlets.interfaces import IPortalFooter, IAboveContentTitle, IAboveContentBody
from Products.CMFPlone.interfaces import IPloneSiteRoot

from Products.ATContentTypes.interface.news import IATNewsItem
from genweb.core.adapters import IImportant

from genweb.core.interfaces import IHomePage
from genweb.core.utils import genweb_config, havePermissionAtRoot, pref_lang

from genweb.theme.browser.interfaces import IGenwebTheme
from genweb.alternatheme.browser.viewlets import gwManagePortletsFallbackViewlet
from vilaix.theme.browser.interfaces import IVilaixTheme

from plone.app.collection.interfaces import ICollection
from genweb.core import HAS_CAS
from zope.security import checkPermission

import random
from genweb.core import GenwebMessageFactory as _
from DateTime.DateTime import DateTime

grok.context(Interface)


class viewletBase(grok.Viewlet):
    grok.baseclass()

    @memoize_contextless
    def portal_url(self):
        return self.portal().absolute_url()

    @memoize_contextless
    def portal(self):
        return getSite()

    def genweb_config(self):
        return genweb_config()

    def pref_lang(self):
        """ Extracts the current language for the current user
        """
        lt = getToolByName(self.portal(), 'portal_languages')
        return lt.getPreferredLanguage()


class gwPersonalBarViewlet(PersonalBarViewlet, viewletBase):
    grok.name('genweb.personalbar')
    grok.viewletmanager(IPortalTop)
    grok.layer(IVilaixTheme)

    index = ViewPageTemplateFile('viewlets_templates/personal_bar.pt')

    def showRootFolderLink(self):
        return havePermissionAtRoot()

    def canManageSite(self):
        return checkPermission("plone.app.controlpanel.Overview", self.portal())

    def getPortraitMini(self):
        pm = getToolByName(self.portal(), 'portal_membership')
        return pm.getPersonalPortrait().absolute_url()

    def logout_link(self):
        if HAS_CAS:
            return '{}/cas_logout'.format(self.portal_url)
        else:
            return '{}/logout'.format(self.portal_url)


class gwHeader(viewletBase):
    grok.name('genweb.header')
    grok.template('header')
    grok.viewletmanager(IPortalHeader)
    grok.layer(IVilaixTheme)

    def get_image_class(self):
        if self.genweb_config().treu_menu_horitzontal:
            # Is a L2 type
            return 'l2-image'
        else:
            return 'l3-image'

    def show_login(self):
        isAnon = getMultiAdapter((self.context, self.request), name='plone_portal_state').anonymous()
        return not self.genweb_config().amaga_identificacio and isAnon

    def pref_lang(self):
        """ Extracts the current language for the current user
        """
        lt = getToolByName(self.portal(), 'portal_languages')
        lang = lt.getDefaultLanguage()

        if lang == 'ca':
            pref_lang = 'Català'
        elif lang == 'es':
            pref_lang = 'Español'
        elif lang == 'en':
            pref_lang = 'English'

        return pref_lang

    def languages(self):
        portal = getSite()
        pl = getToolByName(portal, 'portal_languages')
        return pl.supported_langs

    def getDadesLanguages(self):
        portal = getSite()
        urltool = portal.absolute_url()
        pl = getToolByName(portal, 'portal_languages')
        langs_supported = pl.getSupportedLanguages()
        pref_lang = pl.getPreferredLanguage()
        default_lang = pl.getDefaultLanguage()
        dades = []
        languages = [{'lang': 'ca', 'valor': 'Català'},{'lang': 'es', 'valor': 'Español'},{'lang': 'en', 'valor': 'English'}]

        for i in langs_supported:
            if i in default_lang:
                for x in languages:
                    if x['lang'] in i:
                        literal=x['valor']
                dades.append(dict(url="%s?set_language=%s" % (urltool, default_lang),
                                  lang=default_lang,
                                  literal=literal,
                                  google_translated=False
                                  )
                            )
            else:
                for x in languages:
                    if x['lang'] in i:
                        literal=x['valor']
                dades.append(dict(url="http://translate.google.com/translate?hl=%s&sl=%s&tl=%s&u=%s" % (default_lang, default_lang, i, urltool),
                                  lang = i,
                                  literal=literal,
                                  google_translated=True
                                  )
                            )

        return dades

    # def show_directory(self):
    #     return self.genweb_config().directori_upc

    # def get_image_capsalera(self):
    #     #Obté totes les imatges de la carpeta imatges-capcalera i fa un random retornant una cada cop
    #     urltool = getToolByName(self.context, 'portal_url')
    #     portal_catalog = getToolByName(self.context, 'portal_catalog')
    #     path = urltool.getPortalPath() + '/imatges-capcalera'
    #     resultats = []
    #     #Imatge capcalera per defecte
    #     style = 'background-image: url("/++vilaix++static/images/capcalera.jpg")'

    #     imatges = self.context.portal_catalog.searchResults(portal_type='Image',
    #                                                         path=path)
    #     if imatges.actual_result_count != 0:
    #         imatge = random.choice(imatges)
    #         style = 'background-image: url(' + imatge.getPath() +')'

    #     return style


class randomImage(viewletBase):
    grok.name('vilaix.randomImage')
    grok.template('randomImage')
    grok.viewletmanager(IPortalHeader)
    grok.layer(IVilaixTheme)

    def get_image_class(self):
        if self.genweb_config().treu_menu_horitzontal:
            # Is a L2 type
            return 'l2-image'
        else:
            return 'l3-image'

    def show_login(self):
        isAnon = getMultiAdapter((self.context, self.request), name='plone_portal_state').anonymous()
        return not self.genweb_config().amaga_identificacio and isAnon

    # def show_directory(self):
    #     return self.genweb_config().directori_upc

    def get_image_capsalera(self):
        style = 'background-image: url(/++vilaix++static/images/capcalera.jpg)'
        imatges = []

        if IPloneSiteRoot.providedBy(self.context):
            style = 'background-image: url(/++vilaix++static/images/fons_vilaix.png);height: 0px;'
        else:
            #Obté totes les imatges de la carpeta imatges-capcalera i fa un random retornant una cada cop
            urltool = getToolByName(self.context, 'portal_url')
            portal_catalog = getToolByName(self.context, 'portal_catalog')
            path = urltool.getPortalPath() + '/material-multimedia/imatges-capcalera'
            contenido = self.context

            if contenido.portal_type == 'Collection' and contenido.getLayout() == 'subhome':
                filtre = contenido.query
                etiqueta = []
                #Dades filtre --> [{u'i': u'Subject', u'o': u'plone.app.querystring.operation.selection.is', u'v': [u'prova']}]
                if filtre == None:
                    etiqueta.append('general')
                else:
                    for i in filtre:
                        if i['i'] == 'Subject':
                            etiquetas = i['v']
                            num = len(etiquetas)
                            for n in range(num):
                                etiqueta.append(etiquetas[n].encode())

                imatges = self.context.portal_catalog.searchResults(portal_type='Image',path=path, Subject=etiqueta)
            elif len(contenido.subject) > 0:
                etiqueta = []
                etiquetas = contenido.subject
                num = len(contenido.subject)
                for n in range(num):
                    etiqueta.append(etiquetas[n].encode())
                imatges = self.context.portal_catalog.searchResults(portal_type='Image',path=path, Subject=etiqueta)
            else:
                style = 'background-image: url(/++vilaix++static/images/capcalera.jpg)'
                imatges = self.context.portal_catalog.searchResults(portal_type='Image',
                                                                    path=path)

                values = self.context.portal_catalog.uniqueValuesFor('Subject')


            if imatges.actual_result_count != 0:
                imatge = random.choice(imatges)
                style = 'background-image: url(' + imatge.getPath() +')'

        return style


class slider(viewletBase):
    grok.context(IPloneSiteRoot)
    grok.name('vilaix.slider')
    grok.template('slider')
    grok.viewletmanager(IPortalHeader)
    grok.layer(IVilaixTheme)

    def sliderItems(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        utool = getToolByName(self.context, 'portal_url')
        path = '{0}/material-multimedia/sliders'.format(utool.getPortalPath()),
        now = DateTime()

        items = catalog.searchResults(portal_type='Slider',
                                      path=dict(query=path, depth=1),
                                      review_state='published',
                                      Subject='principal',
                                      expires={'query': now, 'range': 'min', },
                                      sort_on='getObjPositionInParent')

        results = []
        for item in items:
            results.append(
                {'img': '%s/@@images/image' % (item.getURL()),
                 'title': item.Title,
                 'text': item.Description,
                 'alt': item.getObject().alt,
                 'url': item.getObject().remoteUrl,
                 'target': item.open_link_in_new_window and '_blank' or None,
                 }
            )

        return results


class collectionFallbackViewlet(gwManagePortletsFallbackViewlet):
    grok.context(ICollection)
    grok.name('plone.manage_portlets_fallback')
    grok.viewletmanager(IBelowContent)
    grok.layer(IVilaixTheme)

    render = ViewPageTemplateFile('viewlets_templates/manage_portlets_fallback.pt')

# class gwImportantNews(viewletBase):
#     grok.name('genweb.important')
#     grok.context(IATNewsItem)
#     grok.template('important')
#     grok.viewletmanager(IAboveContentTitle)
#     grok.layer(IGenwebTheme)

#     def permisos_important(self):
#         #TODO: Comprovar que l'usuari tingui permisos per a marcar com a important
#         return not IImportant(self.context).is_important and getSecurityManager().checkPermission("plone.app.controlpanel.Overview", self.portal)

#     def permisos_notimportant(self):
#         #TODO: Comprovar que l'usuari tingui permisos per a marcar com a important
#         return IImportant(self.context).is_important and getSecurityManager().checkPermission("plone.app.controlpanel.Overview", self.portal)

#     def update(self):
#         form = self.request.form
#         if 'genweb.theme.viewlet.marcar_important' in form:
#             IImportant(self.context).is_important = True
#         if 'genweb.theme.viewlet.marcar_notimportant' in form:
#             IImportant(self.context).is_important = False


class gwGlobalSectionsViewlet(GlobalSectionsViewlet, viewletBase):
    grok.name('genweb.globalsections')
    grok.viewletmanager(IPortalTop)
    grok.layer(IVilaixTheme)

    index = ViewPageTemplateFile('viewlets_templates/sections.pt')

    allowed_section_types = ['Folder', 'Collection', 'Document']

    def show_menu(self):
        return not self.genweb_config().treu_menu_horitzontal and self.portal_tabs

    def menuPrincipal(self):
        """ returns folders (menu-principal)"""
        urltool = getToolByName(self.context, 'portal_url')
        portal_catalog = getToolByName(self.context, 'portal_catalog')
        # Obtain all folders in first level "published" o "visible"
        path = urltool.getPortalPath() + '/menu-principal'
        folders = portal_catalog.searchResults(portal_type=self.allowed_section_types,
                                               path=dict(query=path, depth=1),
                                               sort_on='getObjPositionInParent')
        results = []
        for fold in folders:
            if (fold.portal_type in self.allowed_section_types):
                if fold.exclude_from_nav is not True:
                    results.append(dict(name=fold.Title,
                                        url=fold.getURL(),
                                        id=fold.getId,
                                        description=fold.Description))

        return results

    def menu(self):
        """ returns subfolders (submenus) for the dropdown in navbar"""
        urltool = getToolByName(self.context, 'portal_url')
        portal_catalog = getToolByName(self.context, 'portal_catalog')
        # Obtain all folders in first level "published" o "visible"
        path = urltool.getPortalPath() + '/menu-principal'
        folders = portal_catalog.searchResults(portal_type=self.allowed_section_types,
                                               path=dict(query=path, depth=1),
                                               sort_on='getObjPositionInParent')

        subfolders = {}
        for fold in folders:
            if (fold.portal_type in self.allowed_section_types):
                if fold.exclude_from_nav is not True:
                    subfolders[fold.getId] = self.SubMenu(fold.getPath())
        return subfolders

    def SubMenu(self, path):
        """ Get subfolders of current folder for create submenu"""
        path = path
        portal_catalog = getToolByName(self.context, 'portal_catalog')
        subfolders = portal_catalog.searchResults(portal_type=self.allowed_section_types,
                                                  path=dict(query=path, depth=1),
                                                  sort_on='getObjPositionInParent')

        results = []
        for fold in subfolders:
            if (fold.portal_type in self.allowed_section_types):
                if fold.exclude_from_nav is not True:
                    results.append(dict(name=fold.Title,
                                        url=fold.getURL(),
                                        id=fold.getId,
                                        description=fold.Description))

        return results

# class gwPathBarViewlet(PathBarViewlet, viewletBase):
#     grok.name('genweb.pathbar')
#     grok.viewletmanager(IPortalTop)
#     grok.layer(IGenwebTheme)

#     index = ViewPageTemplateFile('viewlets_templates/path_bar.pt')


class gwFooter(viewletBase):
    grok.name('genweb.footer')
    grok.template('footer')
    grok.viewletmanager(IPortalFooter)
    grok.layer(IVilaixTheme)

    def getLinksPeu(self):
        """ links fixats per accessibilitat/rss/about """
        idioma = self.pref_lang()
        footer_links = {
            "ca": {
                "rss": "rss-ca",
                "about": "sobre-aquest-web",
                "accessibility": "accessibilitat"
            },
            "es": {
                "rss": "rss-es",
                "about": "sobre-esta-web",
                "accessibility": "accesibilidad"
            },
            "en": {
                "rss": "rss-en",
                "about": "about-this-web",
                "accessibility": "accessibility"
            },
            # "zh": {
            #     "rss": "rss-en",
            #     "about": "about-this-web",
            #     "accessibility": "accessibility"
            # },
        }

        return footer_links[idioma]


# class gwSearchViewletManager(grok.ViewletManager):
#     grok.context(Interface)
#     grok.name('genweb.search_manager')


# class gwSearchViewlet(SearchBoxViewlet, viewletBase):
#     grok.context(Interface)
#     grok.viewletmanager(gwSearchViewletManager)
#     grok.layer(IGenwebTheme)

#     render = ViewPageTemplateFile('viewlets_templates/searchbox.pt')


# class gwManagePortletsFallbackViewlet(ManagePortletsFallbackViewlet, viewletBase):
#     """ The override for the manage_portlets_fallback viewlet for IPloneSiteRoot
#     """
#     grok.context(IPloneSiteRoot)
#     grok.name('plone.manage_portlets_fallback')
#     grok.viewletmanager(IBelowContent)
#     grok.layer(IGenwebTheme)

#     render = ViewPageTemplateFile('viewlets_templates/manage_portlets_fallback.pt')

#     def getPortletContainerPath(self):
#         context = aq_inner(self.context)
#         pc = getToolByName(context, 'portal_catalog')
#         result = pc.searchResults(object_provides=IHomePage.__identifier__,
#                                   Language=pref_lang())
#         if result:
#             return result[0].getURL()
#         else:
#             # If this happens, it's bad. Implemented as a fallback
#             return context.absolute_url()

#     def managePortletsURL(self):
#         return "%s/%s" % (self.getPortletContainerPath(), '@@manage-homeportlets')

#     def available(self):
#         secman = getSecurityManager()
#         if secman.checkPermission('Portlets: Manage portlets', self.context):
#             return True
#         else:
#             return False


class TitleViewlet(TitleViewlet, viewletBase):
    grok.context(Interface)
    grok.name('plone.htmlhead.title')
    grok.viewletmanager(IHtmlHead)
    grok.layer(IVilaixTheme)

    def update(self):
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        context_state = getMultiAdapter((self.context, self.request), name=u'plone_context_state')
        page_title = escape(safe_unicode(context_state.object_title()))
        portal_title = escape(safe_unicode(portal_state.navigation_root_title()))

        genweb_title = getattr(self.genweb_config(), 'html_title_%s' % self.pref_lang(), 'Genweb Vilaix')
        if not genweb_title:
            genweb_title = 'Genweb Vilaix'
        genweb_title = escape(safe_unicode(re.sub(r'(<.*?>)', r'', genweb_title)))

        if page_title == portal_title:
            self.site_title = u"%s" % (genweb_title)
        else:
            self.site_title = u"%s &mdash; %s" % (page_title, genweb_title)
