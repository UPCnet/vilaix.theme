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

    def abrevia(self, summary, sumlenght):
        """ Retalla contingut de cadenes
        """
        bb = ''

        if sumlenght < len(summary):
            bb = summary[:sumlenght]

            lastspace = bb.rfind(' ')
            cutter = lastspace
            precut = bb[0:cutter]

            if precut.count('<b>') > precut.count('</b>'):
                cutter = summary.find('</b>', lastspace) + 4
            bb = summary[0:cutter]
            if precut.count('<strong>') > precut.count('</strong>'):
                cutter = summary.find('</strong>', lastspace) + 9
            bb = summary[0:cutter]

            if bb.count('<p') > precut.count('</p'):
                bb += '...</p>'
            else:
                bb = bb + '...'
        else:
            bb = summary

        return bb
