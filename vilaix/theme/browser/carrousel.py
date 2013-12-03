# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

class carrousel(ViewletBase):
    render = ViewPageTemplateFile('viewlets_templates/carrousel.pt')
    
    def getElementsCarrousel(self):
        """ Retorna tots els objectes de tipus Carrousel que hi ha a la carpeta carrousel
        """
        urltool = getToolByName(self.context, 'portal_url')        
        portal_catalog = getToolByName(self, 'portal_catalog')
        path = urltool.getPortalPath()   
        lt = getToolByName(self, 'portal_languages')
        nElements = 4
        llistaElementsCarrousel = []  
        # Cerca contingut per mostar al carousel en diversos idiomes
        #path = path + '/carrousel-'+ lt.getPreferredLanguage() +'/carrousel/',
        elementsCarrousel = portal_catalog.searchResults(portal_type = 'Carrousel',
                                               path = path + '/carrousel',
                                               review_state = 'published',
                                               sort_on='getObjPositionInParent')
                                                        
        if len(elementsCarrousel) > 0:
            #Retorna una llista amb els elementsCarrousel en blocs de 4 elements
            llistaElementsCarrousel=[elementsCarrousel[i:i+nElements] for i in range(0,len(elementsCarrousel),nElements)]
        
        return llistaElementsCarrousel

    def getBlocs(self):
        llistaElementsCarrousel = self.getElementsCarrousel()
        return len(llistaElementsCarrousel)

       
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