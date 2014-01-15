# -*- coding: utf-8 -*-
from five import grok
from plone.memoize.view import memoize_contextless
from zope.component.hooks import getSite
from vilaix.core.interfaces import IEquipament
from Products.CMFCore.utils import getToolByName

class View(grok.View):
    grok.context(IEquipament)
    grok.require('zope2.View')

    @memoize_contextless
    def portal_url(self):
        return self.portal().absolute_url()

    @memoize_contextless
    def portal(self):
        return getSite()

    def getImage(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        utool = getToolByName(self.context, 'portal_url')
        
        url = self.request.getURL()

        url_imatge = '%s/++widget++form.widgets.image/@@download/%s' % (url.replace("view", "@@edit"), self.context.image.filename)
       
        return url_imatge
    
    def getMapa(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        utool = getToolByName(self.context, 'portal_url')
       
        caracter = "+"
        adreca_cont = ''
        cp = ''
        poblacio = ''

        if self.context.adreca_contacte:
            adreca_cont = self.context.adreca_contacte.split()
        
        if self.context.codi_postal:
            cp = self.context.codi_postal.split()
        
        if self.context.poblacio:
            poblacio = self.context.poblacio.split()
        
        adreca = caracter.join(adreca_cont) + '+' + caracter.join(cp) + '+' + caracter.join(poblacio)

        mapa = '<iframe width="425" height="350" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="https://maps.google.es/maps?f=q&amp;source=s_q&amp;hl=ca&amp;geocode=&amp;q=%s;aq=&amp;ie=UTF8&amp;hq=&amp;hnear=%s;t=m&amp;z=14&amp;iwloc=A&amp;output=embed"></iframe>' % (adreca, adreca)
        return mapa


