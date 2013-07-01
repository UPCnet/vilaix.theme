# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

class carrousel(ViewletBase):
    render = ViewPageTemplateFile('viewlets_templates/carrousel.pt')
    
    def getImatges(self):
        """ Retorna les imatges per mostar al carousel
        """
        urltool = getToolByName(self.context, 'portal_url')        
        portal_catalog = getToolByName(self, 'portal_catalog')
        path = urltool.getPortalPath()   
        lt = getToolByName(self, 'portal_languages')
        # Cerca contingut per mostar al carousel en diversos idiomes
        #path = path + '/config-'+ lt.getPreferredLanguage() +'/carrousel/',
        imatges = portal_catalog.searchResults(portal_type = 'Carrousel',
                                               path = path + '/config'+ '/carrousel/',
                                               sort_on='getObjPositionInParent')
        
        return imatges
       
    def getAltAndTitle(self, altortitle):
        """Funcio que extreu idioma actiu i afegeix al alt i al title de les imatges del banner
           el literal Obriu enllac en una finestra nova
        """
        lt = getToolByName(self, 'portal_languages')
        idioma = lt.getPreferredLanguage()
        str = ''
        if idioma == 'ca':
            str = "Obriu l'enllaç en una finestra nova"
        if idioma == 'es':
            str = "Abre en ventana nueva"
        if idioma == 'en':
            str = "Open in new window"
        if str == '':
            str = "Obriu l'enllaç en una finestra nova"
        return altortitle + ', ' + str

    def portal_url(self):        
        return self.context.absolute_url()