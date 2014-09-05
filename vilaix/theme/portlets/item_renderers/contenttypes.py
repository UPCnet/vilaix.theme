# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from interfaces import IPortletItemRenderer
from renderer import PortletItemRenderer
from Products.CMFCore.utils import getToolByName

from plone.app.contenttypes.interfaces import IEvent
from plone.app.contenttypes.interfaces import INewsItem
from plone.app.contenttypes.interfaces import IFile
from five.grok import adapter
from five.grok import implementer

from Products.CMFCore.interfaces import IContentish
from DateTime.DateTime import DateTime
from Acquisition import aq_inner

from genweb.core import GenwebMessageFactory as TAM

from vilaix.core.content.equipament import IEquipament
from vilaix.core.content.tramit import ITramit
from vilaix.core.content.slider import ISlider
from upc.genweb.banners.content.interfaces import IBanner

from zope.i18nmessageid import MessageFactory
PLMF = MessageFactory('plonelocales')


@adapter(IContentish)
@implementer(IPortletItemRenderer)
class DefaultPortletItemRenderer(PortletItemRenderer):
    template = ViewPageTemplateFile('default.pt')
    css_class = 'contentish-item'


@adapter(IEvent)
@implementer(IPortletItemRenderer)
class EventPortletItemRenderer(PortletItemRenderer):
    template = ViewPageTemplateFile('event.pt')
    css_class = 'multidate'

    def sameDay(self):
        if DateTime.Date(self.item.start) == DateTime.Date(self.item.end):
            return True
        else:
            return False

    def getText(self):
        #return self.cropText(self.item.getObject().SearchableText(), 100)
        return self.cropText(self.item.getObject().Description(), 100)

    def getMonthAbbr(self, data):
        context = aq_inner(self.context)
        month = DateTime.month(data)
        self._ts = getToolByName(context, 'translation_service')
        monthName = TAM(self._ts.month_msgid(month, format='a'),
                              default=self._ts.month_english(month, format='a'))
        return monthName

    def getMonth(self, data):
        context = aq_inner(self.context)
        month = DateTime.month(data)
        self._ts = getToolByName(context, 'translation_service')
        monthName = PLMF(self._ts.month_msgid(month),
                              default=self._ts.month_english(month))
        return monthName

    def getDay(self, data):
        day = str(DateTime.day(data))
        return day


@adapter(INewsItem)
@implementer(IPortletItemRenderer)
class NewsPortletItemRenderer(PortletItemRenderer):
    template = ViewPageTemplateFile('newsitem.pt')
    css_class = 'noticies clearfix'

    def getText(self):
        return self.cropText(self.item.getObject().text.raw, 230)


@adapter(IEquipament)
@implementer(IPortletItemRenderer)
class EquipamentPortletItemRenderer(PortletItemRenderer):
    template = ViewPageTemplateFile('equipament.pt')
    css_class = 'equipament clearfix'


@adapter(ITramit)
@implementer(IPortletItemRenderer)
class TramitPortletItemRenderer(PortletItemRenderer):
    template = ViewPageTemplateFile('tramit.pt')
    css_class = 'tramit clearfix'


@adapter(IBanner)
@implementer(IPortletItemRenderer)
class BannerPortletItemRenderer(PortletItemRenderer):
    template = ViewPageTemplateFile('banner.pt')
    css_class = 'banner clearfix'

    def getTarget(self):
        obj = self.item.getObject()
        if obj.Obrirennovafinestra:
            result = '_blank'
        else:
            result = ''
        return result

@adapter(ISlider)
@implementer(IPortletItemRenderer)
class SliderPortletItemRenderer(PortletItemRenderer):
    template = ViewPageTemplateFile('slider.pt')
    css_class = 'slider clearfix'

    def getTarget(self):
        obj = self.item.getObject()
        if obj.Obrirennovafinestra:
            result = '_blank'
        else:
            result = ''
        return result

@adapter(IFile)
@implementer(IPortletItemRenderer)
class EquipamentPortletItemRenderer(PortletItemRenderer):
    template = ViewPageTemplateFile('file.pt')
    css_class = 'file clearfix'
