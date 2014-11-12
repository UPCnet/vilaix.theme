# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from plone import api
from zope.i18nmessageid import MessageFactory
_ = MessageFactory("vilaix")

class carrousel(ViewletBase):
    render = ViewPageTemplateFile('viewlets_templates/carrousel_mobile.pt')

    def getElementsCarrousel(self):
        """ Retorna tots els objectes de tipus Carrousel que hi ha a la carpeta carrousel
        """
        urltool = getToolByName(self.context, 'portal_url')
        portal_catalog = getToolByName(self, 'portal_catalog')
        path = urltool.getPortalPath()
        lt = getToolByName(self, 'portal_languages')
        nElements = 2
        llistaElementsCarrousel = []
        # Cerca contingut per mostar al carousel en diversos idiomes
        #path = path + '/carrousel-'+ lt.getPreferredLanguage() +'/carrousel/',
        elementsCarrousel = portal_catalog.searchResults(portal_type = 'Carrousel',
                                               path = path + 'material-multimedia/carroussel',
                                               sort_on='getObjPositionInParent')

        if len(elementsCarrousel) > 0:
            #Retorna una llista amb els elementsCarrousel en blocs de 4 elements
            llistaElementsCarrousel=[elementsCarrousel[i:i+nElements] for i in range(0,len(elementsCarrousel),nElements)]

        return llistaElementsCarrousel

    def getBlocs(self):
        llistaElementsCarrousel = self.getElementsCarrousel()
        return len(llistaElementsCarrousel)

    def portal(self):
        return api.portal.get()

    def getAltAndTitle(self, altortitle, open_link_in_new_window):
        """Funcio que extreu idioma actiu i afegeix al alt i al title de les imatges del carrousel
           el literal Obriu enllac en una finestra nova
        """
        if open_link_in_new_window:
            return '%s, %s' % (altortitle.decode('utf-8'), self.portal().translate(_('obrir_link_finestra_nova', default=u"(obriu en una finestra nova)")))
        else:
            return '%s' % (altortitle.decode('utf-8'))

    def portal_url(self):
        return self.context.absolute_url()
