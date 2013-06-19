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


class INoticiaDestacadaPortlet(IPortletDataProvider):
    """ Defines a new portlet 
    """


class Assignment(base.Assignment):
    implements(INoticiaDestacadaPortlet)

    def __init__(self, count=1, state=('published', )):
        self.count = count
        self.state = state

    @property
    def title(self):
        return _(u"Noticia Destacada")


class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('templates/noticiaDestacada.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

    @ram.cache(render_cachekey)
    def render(self):
        return xhtml_compress(self._template())
  
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

   
    def retornaDestacats(self):
        """ Mostra la primera noticia destacada
        """
        context = self.context

        destacats = context.portal_catalog.searchResults(portal_type = 'News Item',
                                                         review_state=['published',],
                                                         sort_on='getObjPositionInParent',
                                                        )
        
        destacats = destacats[:1] # Retornem el primer
         
        data = [dict(id=a.id,
                     description =self.abrevia(a.Description,250), 
                     url=a.getURL(),                    
                     title=a.Title,
                     new = a.getObject(),
                     image = a.getObject().image,
                     Text = self.abrevia(a.getObject().text.raw,250)) for a in destacats]

        return data

    @memoize
    def _data(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        portal_state = getMultiAdapter((context, self.request),
            name='plone_portal_state')
        path = portal_state.navigation_root_path()
        limit = self.data.count
        state = self.data.state
        return catalog(portal_type='News Item',
                       review_state=state,
                       path=path,
                       sort_on='Date',
                       sort_order='reverse',
                       sort_limit=limit)[:limit]      
   
class AddForm(base.AddForm):
    form_fields = form.Fields(INoticiaDestacadaPortlet)
    label = _(u"Add News Portlet")
    description = _(u"This portlet displays recent News Items.")

    def create(self, data):
        return Assignment(count=data.get('count', 1), state=data.get('state', ('published', )))


class EditForm(base.EditForm):
    form_fields = form.Fields(INoticiaDestacadaPortlet)
    label = _(u"Edit News Portlet")
    description = _(u"This portlet displays recent News Items.")
