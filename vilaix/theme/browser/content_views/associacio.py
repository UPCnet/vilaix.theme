# -*- coding: utf-8 -*-
from five import grok
from plone.memoize.view import memoize_contextless
from zope.component.hooks import getSite
from urllib import quote
from vilaix.core.content.associacio import IAssociacio


class View(grok.View):
    grok.context(IAssociacio)
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
        #     latitude = self.context.latitude.encode('ascii', 'ignore')
        #     longitude = self.context.longitude.encode('ascii', 'ignore')
        #     mapa = '<iframe width="100%" height="500" src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d11947.36863264995!2d' + longitude + '!3d' + latitude + '!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x29576d35b09bdbce!2sCentre+Civic+El+Vapor!5e0!3m2!1sen!2ses!4v1548176647751" width="800" height="600" frameborder="0" style="border:0" allowfullscreen></iframe>'
        #     return mapa

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

            # if self.context.geolocalitzacio:
            #     geolocalitzacio = self.context.geolocalitzacio

            geolocalitzacio = self.context.latitude.encode('ascii', 'ignore') + ',' + self.context.longitude.encode('ascii', 'ignore')

            adreca_postal = caracter.join(adreca) + '+' + caracter.join(cp) + '+' + caracter.join(poblacio_cont)
            # import pdb; pdb.set_trace()
            mapa = '<iframe width="425" height="350" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="https://maps.google.es/maps?f=q&amp;source=s_q&amp;hl=ca&amp;geocode=&amp;q=%s;aq=&amp;sll=%s;ie=UTF8&amp;hnear=%s;radius=15000&amp;t=m&amp;ll=%s;z=14&amp;iwloc=A&amp;output=embed"></iframe>' % (adreca_postal, geolocalitzacio, adreca_postal, geolocalitzacio)
            return mapa


# <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3706.7564439869866!2d2.1800498801323607!3d41.52189389570991!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x12a4be5fb2d9cba7%3A0x782a2a2c1be565ad!2sPasseig+de+Can+Tai%C3%B3%2C+83%2C+08130+Santa+Perp%C3%A8tua+de+Mogoda%2C+Barcelona!5e1!3m2!1sen!2ses!4v1548178000592" width="600" height="450" frameborder="0" style="border:0" allowfullscreen></iframe>
