# -*- coding: utf-8 -*-
from five import grok
from plone.memoize.view import memoize_contextless
from zope.component.hooks import getSite
from vilaix.core.content.equipament import IEquipament
from Products.CMFCore.utils import getToolByName
from urllib import quote

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

        url_imatge = ''

        if self.context.image:
            url_imatge = '%s/++widget++form.widgets.image/@@download/%s' % (url.replace("view", "@@edit"), self.context.image.filename)
       
        return url_imatge
    
    def getMapa(self):

        catalog = getToolByName(self.context, 'portal_catalog')
        utool = getToolByName(self.context, 'portal_url')
        
        """
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
               

            if self.context.geolocalitzacio:
                geolocalitzacio = self.context.geolocalitzacio
            
            adreca_postal = caracter.join(adreca) + '+' + caracter.join(cp) + '+' + caracter.join(poblacio_cont)
                   
            mapa = '<iframe width="425" height="350" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="https://maps.google.es/maps?f=q&amp;source=s_q&amp;hl=ca&amp;geocode=&amp;q=%s;aq=&amp;sll=%s;ie=UTF8&amp;hnear=%s;radius=15000&amp;t=m&amp;ll=%s;z=14&amp;iwloc=A&amp;output=embed"></iframe>' % (adreca_postal, geolocalitzacio, adreca_postal, geolocalitzacio)
            return mapa

        """
        if self.context.latitude and self.context.longitude:

            mapa = """

            <div id='map' style='height:400px;'></div>

            <link href='http://cdn.leafletjs.com/leaflet/v1.0.0-rc.1/leaflet.css' rel='stylesheet'/>

            <script src='http://cdn.leafletjs.com/leaflet/v1.0.0-rc.1/leaflet.js'></script>
            <script src="https://cdn.polyfill.io/v2/polyfill.min.js?features=Promise"></script>

            <script src="++vilaix++js/leaflet-bing-layer.js"></script>

            <script type='text/javascript'>

            var openStreetLayer = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
            maxZoom: 18,
            id: 'mapbox.streets',
            accessToken: 'pk.eyJ1Ijoicm9naXZlbnR1dXBjIiwiYSI6ImNqcGRzejRjdDAxNmkzc3FyZjlvbG5nb2gifQ.IptrsYJTdxFTxVMQeT_XwQ'
            });

            var BING_KEY = 'AuhiCJHlGzhg93IqUH_oCpl_-ZUrIE6SPftlyGYUvr9Amx5nzA-WqGcPquyFZl4L'
            var bingLayer = L.tileLayer.bing(BING_KEY)

            var mapType = {
            "Open Street Maps":openStreetLayer,
            "Bing Maps":bingLayer}

            """

            lat = self.context.latitude.encode('utf-8')
            lon =self.context.longitude.encode('utf-8')

            mapa += """

            var map = L.map('map', {
            center:[%s, %s],
            zoom: 16,
            layers:[openStreetLayer]});        

            L.control.layers(mapType).addTo(map);

            var markIcon = L.icon({
            iconUrl: 'https://i.stack.imgur.com/pQ1Cq.png',
            iconSize:     [30, 30], // size of the icon
            iconAnchor:   [15, 30], // point of the icon which will correspond to marker's location
            popupAnchor:  [0, -30] // point from which the popup should open relative to the iconAnchor
            })

            L.marker([%s, %s],{icon:markIcon}).addTo(map); 

            </script>

            """ % (lat, lon, lat, lon)


        else:
            mapa = "<p>Es necessari informar els camps de Latitud i Longitud</p>"

        return mapa
