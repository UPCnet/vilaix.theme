from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from Acquisition import aq_base, aq_inner
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName

from plone.app.layout.viewlets.common import GlobalSectionsViewlet

class navigationPeu(GlobalSectionsViewlet):
    index = ViewPageTemplateFile('viewlets_templates/navigationPeu.pt')

    def num_carp(self):
        return 'ul' + str(len(self.homePortalTabs()))

    def homePortalTabs(self):
        urltool = getToolByName(self.context, 'portal_url')
        portal_catalog = getToolByName(self.context, 'portal_catalog')
        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        tabs_root = context_state.is_portal_root()
        cont = 1

        path = urltool.getPortalPath() + '/menu-principal'
        folders = portal_catalog.searchResults(portal_type = 'Folder',
                                         path = dict(query=path, depth=1),
                                         review_state=['internally_published','external','published'],
                                         sort_on='getObjPositionInParent')

        results = []
        for fold in folders:
            #if cont <= 4:
                if fold.exclude_from_nav == False:
                    results.append(dict(id_menu_titulo=fold.Title,
                                        id_menu_url=fold.getURL(),
                                        id_menu='m' + str(cont),
                                        sub_menus = [i for i in portal_catalog.searchResults(path = dict(query=fold.getPath(), depth=1),
                                                                                  review_state=['internally_published','external','published'],
                                                                                  sort_on='getObjPositionInParent') if i.exclude_from_nav == False],
                                        id_sub_menus = 'sm' + str(cont),
                                        selected = self.context.absolute_url().startswith(fold.getURL()) and 'selected' or None,
                                        tab_is_root = tabs_root
                                        )
                                   )
                    cont = cont + 1
                else:
                    continue
            #else:
                #continue
        return results
