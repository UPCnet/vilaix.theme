# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('vilaix.core')

from zope.interface import providedBy

from operator import itemgetter


class IMesConsultatPortlet(IPortletDataProvider):
    """ Defines a new portlet 
    """


class Assignment(base.Assignment):
    """ Assigner for portlet. """
    implements(IMesConsultatPortlet)

    title = _(u"Més Consultats", default=u'Més Consultats')
    

class Renderer(base.Renderer):
    
    render = ViewPageTemplateFile('templates/mesConsultat.pt')

    @property
    def available(self):
        """ El portlet només esta disponible a la subhome"""
        return providedBy(self.view)

    def retornaConsultats(self):
        """ Retorna les imatges per mostar al carousel
        """
        urltool = getToolByName(self.context, 'portal_url')        
        portal_catalog = getToolByName(self, 'portal_catalog')
        path = urltool.getPortalPath()

        lt = getToolByName(self, 'portal_languages')
        # if self.context.absolute_url().rfind('ambits') > 0:
        #     etiqueta1 = self.context.esplugues_temes[:-1]
        #     etiqueta2 = self.context.esplugues_persones[:-1]
        #     etiqueta3 = self.context.esplugues_xifres[:-1]
        #     etiqueta4 = self.context.esplugues_barris[:-1]          

        #     documents1 = portal_catalog.searchResults(portal_type = ['Document','Activitat','Servei','Directori','News Item'],
        #                                             review_state= 'published',
        #                                             esplugues_temes = etiqueta1,)
            
        #     documents2 = portal_catalog.searchResults(portal_type = ['Document','Activitat','Servei','Directori','News Item'],
        #                                             review_state= 'published',
        #                                             esplugues_persones = etiqueta2,)

        #     documents3 = portal_catalog.searchResults(portal_type = ['Document','Activitat','Servei','Directori','News Item'],
        #                                             review_state= 'published',
        #                                             esplugues_xifres = etiqueta3,)

        #     documents4 = portal_catalog.searchResults(portal_type = ['Document','Activitat','Servei','Directori','News Item'],
        #                                             review_state= 'published',
        #                                             esplugues_barris = etiqueta4,)
            
        #     documents = documents1 + documents2 + documents3 + documents4

            
        #     data = [dict(title = e.Title,
        #                   target=e.getURL(),
        #                   description=self.abrevia(e.Description,70),
        #                   consultes = e.pageviews)
        #                   for e in documents]              
            
        #     consultats = sorted(data,key=itemgetter('consultes'),reverse=True)

        # else:
        documents = portal_catalog.searchResults(portal_type = ['Document','News Item'],
                                            review_state= 'published',)
        # data = [dict(title = e.Title,
        #           target=e.getURL(),
        #           description=self.abrevia(e.Description,70),
        #           consultes = e.pageviews)
        #           for e in documents]              
    
        # consultats = sorted(data,key=itemgetter('consultes'),reverse=True)

        data = [dict(title = e.Title,
          target=e.getURL(),
          description=self.abrevia(e.Description,70))
          for e in documents]              

        consultats = sorted(data,reverse=True)


        return consultats[:3]

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
    
    
class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()  
