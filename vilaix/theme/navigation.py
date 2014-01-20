from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Acquisition import aq_inner
from zope.component import getMultiAdapter


from plone.app.layout.navigation.root import getNavigationRoot
from Products.CMFPlone.browser.interfaces import INavigationBreadcrumbs
from zope.interface import implements

from Products.Five import BrowserView
from Products.CMFPlone import utils
from Products.CMFPlone.browser.navigation import get_view_url
from Products.CMFPlone.interfaces import IHideFromBreadcrumbs

import re


class PhysicalNavigationBreadcrumbs(BrowserView):
    implements(INavigationBreadcrumbs)

    def breadcrumbs(self):
        real_context = aq_inner(self.context)
        request_path = self.request.get('PATH_INFO', '')
        if 'VirtualHostBase' in request_path:
            path = ('',) + re.search(r'VirtualHostBase/\w+/.*?/(.*?)/VirtualHostRoot/(?:.*?/)?(.*)', request_path).groups()
            request_path = '/'.join(path)
        context_path = '/'.join(real_context.getPhysicalPath())

        if request_path == context_path:
            context = real_context
        else:
            self.context.plone_log(request_path)
            parent_path = request_path[:request_path.rfind('/')]
            self.context.plone_log(parent_path)
            context = self.context.restrictedTraverse(parent_path)
        request = self.request
        container = utils.parent(context)

        name, item_url = get_view_url(context)

        if container is None:
            return (
                {'absolute_url': item_url,
                 'Title': utils.pretty_title_or_id(context, context), },
            )

        view = getMultiAdapter((container, request), name='breadcrumbs_view')
        base = tuple(view.breadcrumbs())

        # Some things want to be hidden from the breadcrumbs
        if IHideFromBreadcrumbs.providedBy(context):
            return base

        if base:
            item_url = '%s/%s' % (base[-1]['absolute_url'], name)

        rootPath = getNavigationRoot(context)
        itemPath = '/'.join(context.getPhysicalPath())

        # don't show default pages in breadcrumbs or pages above the navigation
        # root
        if not utils.isDefaultPage(context, request) \
                and not rootPath.startswith(itemPath):
            base += ({'absolute_url': item_url,
                      'Title': utils.pretty_title_or_id(context, context), },
                     )

        if request_path != context_path:
            name, item_url = get_view_url(real_context)
            base += ({'absolute_url': item_url,
                      'Title': utils.pretty_title_or_id(real_context, real_context), },
                     )

        return base
        return True