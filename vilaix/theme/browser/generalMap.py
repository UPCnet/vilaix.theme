# -*- coding: utf-8 -*-
from five import grok
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from OFS.interfaces import IFolder


class generalMap(grok.View):

    grok.context(IFolder)
    grok.require('zope2.View')

    index = ViewPageTemplateFile("content_views/equipament_templates/viewGeneralMap.pt")

    def render(self):
        return self.index()

    def __call__(self):
        return self.render()

    def getGeneralMap(self):
        mapa = """
            <div id='map' style='height:400px;'></div>
            <link href='//cdn.leafletjs.com/leaflet/v1.0.0-rc.1/leaflet.css' rel='stylesheet'/>
            <script src='//cdn.leafletjs.com/leaflet/v1.0.0-rc.1/leaflet.js'></script>
            <script src="//unpkg.com/leaflet.fullscreen@1.4.5/Control.FullScreen.js"></script>
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

            var map = L.map('map', {
            fullscreenControl: true,
            fullscreenControlOptions: {
              position: 'topleft'
            },
            center:[41.53, 2.18],
            zoom: 16,
            layers:[openStreetLayer]});

            var mapType = {
            "Open Street Maps":openStreetLayer,
            "Bing Maps":bingLayer}

            L.control.layers(mapType).addTo(map);


            var markIcon = L.icon({
            iconUrl: 'https://i.stack.imgur.com/pQ1Cq.png',
            iconSize:     [30, 30], // size of the icon
            iconAnchor:   [15, 30], // point of the icon which will correspond to marker's location
            popupAnchor:  [0, -30] // point from which the popup should open relative to the iconAnchor
            })

        """
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog.searchResults(portal_type="Equipament")
        ordered_params = ('Tipus', 'Telefon', 'Address', 'Horari', 'Correu')
        for brain in brains:
            equipament = brain.getObject()
            if equipament.ubicacio_iframe:
                if not equipament.latitude or not equipament.longitude:
                    continue
                else:
                    if type(equipament.title) == type("str"):
                        equipament.title = equipament.title.decode('utf-8')
                    equip_base_params = dict(
                        lat=equipament.latitude,
                        long=equipament.longitude,
                        title=equipament.title,
                        url=brain.getURL())

                    equip_params = dict(
                        Tipus=equipament.tipus,
                        Telefon=equipament.telefon,
                        Address=equipament.adreca_contacte,
                        Horari=equipament.horari,
                        Correu=equipament.adreca_correu)

                    try:
                        addmark = """
                           L.marker([%(lat)s, %(long)s],{icon:markIcon}).addTo(map)
                            .bindPopup("<a href=%(url)s>%(title)s</a><br>""" % equip_base_params
                    except:
                        continue

                    for i in ordered_params:
                        if equip_params[i]:
                            addmark = addmark + "%s: %s<br>" % (i, equip_params[i])

                    addmark = addmark + """").openPopup();"""
                    addmark = addmark.encode('utf-8')
                    mapa = mapa + addmark

        mapa = mapa + "</script>"
        return mapa
