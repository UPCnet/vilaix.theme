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