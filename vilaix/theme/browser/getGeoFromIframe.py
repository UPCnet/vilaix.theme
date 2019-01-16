# -*- coding: utf-8 -*-
from five import grok
from plone.memoize.view import memoize_contextless
from zope.component.hooks import getSite
from vilaix.core.content.equipament import IEquipament
from Products.CMFCore.utils import getToolByName
from urllib import quote
from plone import api

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class ViewScript(grok.View):
    grok.context(IEquipament)
    grok.require('zope2.View')

    @memoize_contextless
    def portal_url(self):
        return self.portal().absolute_url()

    @memoize_contextless
    def portal(self):
        return getSite()

    index = ViewPageTemplateFile("content_views/equipament_templates/viewGetGeoFromIframe.pt")

    def render(self):
        return self.index()

    def __call__(self):
        return self.render()

    def getGeoFromIframe(self):

        catalog = getToolByName(self.context , 'portal_catalog')
        brains = catalog.searchResults(portal_type="Equipament")
        aux = 0
        for brain in brains:
            equipament = brain.getObject()
            if equipament.ubicacio_iframe:
                try:
                    equipament.latitude = equipament.ubicacio_iframe.raw.split("!3d")[1].split("!")[0]
                    equipament.longitude = equipament.ubicacio_iframe.raw.split("!2d")[1].split("!")[0]
                except:
                    equipament.geolocalitzacio = ""
                    continue

                lat = "{0:.6f}".format(float(equipament.latitude))
                lon = "{0:.6f}".format(float(equipament.longitude))
                equipament.geolocalitzacio = "".join(lat + ", " + lon)
            else:
                equipament.geolocalitzacio = ""