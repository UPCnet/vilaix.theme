# -*- coding: utf-8 -*-
from five import grok
from vilaix.core.content.equipament import IEquipament
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone.utils import _createObjectByType

import csv
import transaction
import unicodedata


class toCsv_script(grok.View):

    grok.context(IEquipament)
    grok.require('zope2.View')

    index = ViewPageTemplateFile("content_views/equipament_templates/viewToCSV.pt")

    def render(self):
        return self.index()

    def __call__(self):
        return self.render()

    def convertToCsv(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog.searchResults(portal_type="Equipament")

        with open('equipaments.csv', 'w') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';')
            spamwriter.writerow(['title', 'geolocalitzacio'])
            for brain in brains:
                equipament = brain.getObject()
                try:
                    title = equipament.title.encode('utf-8')
                except:
                    title = equipament.title
                geo = equipament.geolocalitzacio
                spamwriter.writerow([title, geo])

    def csvEquipToAsso(self):
        # llamar vista en la carpeta de associaciones
        catalog = getToolByName(self.context, 'portal_catalog')

        with open('/tmp/associacions.csv', 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                try:
                    equipToAsso = catalog.searchResults({'portal_type': 'Equipament', 'Title': row[0]})[0].getObject()
                    # creem una nova associacio amb els valors daquest equipament
                    asso = _createObjectByType("Associacio", self.context, equipToAsso.id)
                except:
                    continue

                asso.title = equipToAsso.title
                asso.description = equipToAsso.description
                asso.tipus = equipToAsso.tipus
                asso.telefon = equipToAsso.telefon
                asso.adreca_contacte = equipToAsso.adreca_contacte
                asso.horari = equipToAsso.horari
                asso.adreca_correu = equipToAsso.adreca_correu
                asso.codi_postal = equipToAsso.codi_postal
                asso.poblacio = equipToAsso.poblacio
                asso.mes_informacio = equipToAsso.mes_informacio

                # agafar tambe imatge + etiquetes
                asso.image = equipToAsso.image
                keys = unicodedata.normalize('NFKD', unicode(row[1].lower(), "utf-8")).encode('ascii', errors='ignore')
                asso.subject = (keys, )

                try:
                    asso.latitude = row[2].split(", ")[0]
                    asso.longitude = row[2].split(", ")[1]
                    asso.geolocalitzacio = asso.latitude + ", " + asso.longitude
                except:
                    continue

                asso.ubicacio_iframe = equipToAsso.ubicacio_iframe

                transaction.commit()
                asso.reindexObject()

                # delete from equipments
                print "Deleting: " + equipToAsso.absolute_url_path()
                # equipToAsso.aq_parent.manage_delObjects([equipToAsso.id])

    def getLablesFromCsv(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        with open('/tmp/labels.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)

            assoToDelete = []
            for row in reader:
                try:
                    asso = catalog.searchResults({'portal_type': 'Associacio', 'Title': row[0]})[0].getObject()
                except:
                    assoToDelete.append(row[0])
                    continue
                asso.subject = (row[1].lower(), )
                transaction.commit()
                asso.reindexObject()

    def imgToAsso(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        getAllAssos = catalog.searchResults({'portal_type': 'Associacio'})
        for asso in getAllAssos:
            obj = asso.getObject()
            try:
                equip = catalog.searchResults({'portal_type': 'Equipament', 'Title': obj.id})[0].getObject()
                if equip.image:
                    obj.image = equip.image
            except:
                continue
