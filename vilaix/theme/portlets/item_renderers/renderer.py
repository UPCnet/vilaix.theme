class PortletItemRenderer(object):

    def __init__(self, context):
        self.item = context

    def __call__(self, portletrenderer, **kwargs):
        self.portlet = portletrenderer
        self.request = portletrenderer.request
        self.context = portletrenderer.context

        for key, value in kwargs.items():
            setattr(self, key, value)

        return self.template(self)

    def rendererClass(self):
        return self.css_class

