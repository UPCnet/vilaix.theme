# -*- coding: utf-8 -*-
from five import grok
from plone.memoize.view import memoize_contextless
from zope.component.hooks import getSite
from vilaix.core.content.tramit import ITramit


class View(grok.View):
    grok.context(ITramit)
    grok.require('zope2.View')

    @memoize_contextless
    def portal_url(self):
        return self.portal().absolute_url()

    @memoize_contextless
    def portal(self):
        return getSite()

    def getFitxer(self):
        url = self.request.getURL()
        if self.context.fitxer_inici:
            url_fitxer = '%s/++widget++form.widgets.fitxer_inici/@@download/%s' % (url.replace("view", "@@edit"), self.context.fitxer_inici.filename)
        else:
            url_fitxer = ''

        return url_fitxer

    def fitxers_addicionals(self):
        fitxers = self.context.contentItems()
        url = self.request.getURL()
        results = []
        for fitxer in fitxers:
            url_fitxer = '%s/@@download/file/%s' % (url.replace("view", fitxer[0]), fitxer[1].file.filename)
            dades = {'filename': fitxer[1].file.filename,
                     'url_fitxer': url_fitxer}
            results.append(dades)

        return results
