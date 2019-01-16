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

import csv

from Products.CMFPlone.utils import _createObjectByType


class toCsv_script(grok.View):

    grok.context(IEquipament)
    grok.require('zope2.View')

    index = ViewPageTemplateFile("content_views/equipament_templates/viewToCSV.pt")

    def render(self):
        return self.index()

    def __call__(self):
        return self.render()

    def convertToCsv(self):

        import pdb; pdb.set_trace()
    
        catalog = getToolByName(self.context , 'portal_catalog')
        brains = catalog.searchResults(portal_type="Equipament")

        with open('equipaments.csv' , 'w') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',')
            spamwriter.writerow(['title','geolocalitzacio'])
            for brain in brains:
                equipament = brain.getObject()
                try:
                    title = equipament.title.encode('utf-8')
                except:
                    title = equipament.title
                geo = equipament.geolocalitzacio
                spamwriter.writerow([title,geo])

    def CsvEquipToAsso(self):
        #llamar vista en la carpeta de associaciones

        #self.context.portal_types.listContentTypes()
        catalog = getToolByName(self.context , 'portal_catalog')

        import pdb; pdb.set_trace()
        with open('associacions.csv' , 'r') as csvfile:
            reader = csv.reader(csvfile)

            for row in reader:
                
                try:
                    equipToAsso = catalog.searchResults({'portal_type':'Equipament','Title':row[0]})[0].getObject()
                    #creem una nova associacio amb els valors daquest equipament
                    asso = _createObjectByType("Associacio", self.context, equipToAsso.id)

                except:
                    continue

                asso.title = equipToAsso.title
                asso.tipus = equipToAsso.tipus
                asso.telefon = equipToAsso.telefon
                asso.adreca_contacte = equipToAsso.adreca_contacte
                asso.horari = equipToAsso.horari
                asso.adreca_correu = equipToAsso.adreca_correu
                asso.codi_postal = equipToAsso.codi_postal
                asso.poblacio = equipToAsso.poblacio
                asso.mes_informacio = equipToAsso.mes_informacio

                try:
                    asso.geolocalitzacio = equipToAsso.geolocalitzacio
                    asso.latitude = equipToAsso.latitude
                    asso.longitude = equipToAsso.longitude

                except:
                    asso.latitude = row[1].split(", ")[0]
                    asso.longitude = row[1].split(", ")[1]
                    asso.geolocalitzacio = asso.latitude + ", " + asso.longitude

                asso.ubicacio_iframe = equipToAsso.ubicacio_iframe

                #delete from equipments
                equipToAsso.aq_parent.manage_delObjects([equipToAsso.id])




        

