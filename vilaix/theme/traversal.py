from plone.resource.traversal import ResourceTraverser


class VilaixThemeTraverser(ResourceTraverser):
    """The vilaix theme traverser.

    Allows traversal to /++VilaixTheme++<name> using ``plone.resource`` to fetch
    things stored either on the filesystem or in the ZODB.
    """

    name = 'vilaix'
