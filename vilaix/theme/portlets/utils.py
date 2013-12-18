from zope.component import queryUtility
from zope.component import getMultiAdapter

from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping

from genweb.portlets.browser.manager import ISpanStorage


def setPortletAssignment(pm, context, assID, klass, span=False):
    target_manager = queryUtility(IPortletManager, name='genweb.portlets.HomePortletManager{0}'.format(pm), context=context)
    assignments = getMultiAdapter((context, target_manager), IPortletAssignmentMapping)

    #Assign a new portlet if it's not assigned yet
    if assID not in assignments:
        assignments[assID] = klass()

    #Set portlet width
    if span is not False:
        spanstorage = getMultiAdapter((context, target_manager), ISpanStorage)
        spanstorage.span = str(span)

    return assignments[assID]


def setupQueryPortlet(assignment, header, query, limit, random, more):
    assignment.header = header
    assignment.query = query
    assignment.limit = limit
    assignment.random = random
    assignment.more = more


def setupNavPortlet(assignment, header, bottomLevel):
    assignment.header = header
    assignment.bottomLevel = bottomLevel
