# -*- coding: utf-8 -*-
from five import grok
from plone.memoize.view import memoize_contextless
from zope.component.hooks import getSite
from urllib import quote
from vilaix.core.content.equipament import IEquipament


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
        url = self.request.getURL()
        url_imatge = ''
        if self.context.image:
            url_imatge = '%s/++widget++form.widgets.image/@@download/%s' % (url.replace("view", "@@edit"), self.context.image.filename)

        return url_imatge

    def getMapa(self):
        if self.context.ubicacio_iframe:
            return self.context.ubicacio_iframe.raw
        else:
            caracter = "+"
            adreca_cont = ''
            cp = ''
            poblacio = ''
            geolocalitzacio = ''
            adreca = []
            poblacio_cont = []

            if self.context.adreca_contacte:
                adreca_cont = self.context.adreca_contacte.split()
                for i in range(len(adreca_cont)):
                    adreca_cont_utf8 = quote(adreca_cont[i].encode('utf-8'))
                    adreca.append(adreca_cont_utf8)

            if self.context.codi_postal:
                cp = self.context.codi_postal.split()

            if self.context.poblacio:
                poblacio = self.context.poblacio.split()
                for i in range(len(poblacio)):
                    poblacio_utf8 = quote(poblacio[i].encode('utf-8'))
                    poblacio_cont.append(poblacio_utf8)

            if self.context.latitude and self.context.longitude:
                geolocalitzacio = self.context.latitude.encode('ascii', 'ignore') + ',' + self.context.longitude.encode('ascii', 'ignore')

                adreca_postal = caracter.join(adreca) + '+' + caracter.join(cp) + '+' + caracter.join(poblacio_cont)

                mapa = '<iframe width="425" height="350" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="https://maps.google.es/maps?f=q&amp;source=s_q&amp;hl=ca&amp;geocode=&amp;q=%s;aq=&amp;sll=%s;ie=UTF8&amp;hnear=%s;radius=15000&amp;t=m&amp;ll=%s;z=14&amp;iwloc=A&amp;output=embed"></iframe>' % (adreca_postal, geolocalitzacio, adreca_postal, geolocalitzacio)
                return mapa
            return None
