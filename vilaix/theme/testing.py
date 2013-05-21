from zope.configuration import xmlconfig

from plone.testing.z2 import ZSERVER_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting


class VilaixTheme(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import genweb.theme
        import vilaix.theme
        import genweb.core
        xmlconfig.file('configure.zcml',
                       genweb.theme,
                       context=configurationContext)

        xmlconfig.file('configure.zcml',
                       vilaix.theme,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        applyProfile(portal, 'genweb.theme:default')
        applyProfile(portal, 'genweb.controlpanel:default')
        applyProfile(portal, 'vilaix.theme:default')


VilaixTheme_FIXTURE = VilaixTheme()
VilaixTheme_INTEGRATION_TESTING = IntegrationTesting(
    bases=(VilaixTheme_FIXTURE,),
    name="VilaixTheme:Integration")
VilaixTheme_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(VilaixTheme_FIXTURE,),
    name="VilaixTheme:Functional")
VilaixTheme_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(VilaixTheme_FIXTURE, ZSERVER_FIXTURE),
    name="VilaixTheme:Acceptance")
