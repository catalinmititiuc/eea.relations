""" Control Panel
"""
from zope.component import queryUtility
from zope.interface import implements
from eea.relations.controlpanel.interfaces import IRelationsSettings
from eea.relations.controlpanel.interfaces import _
from plone.app.controlpanel.form import ControlPanelForm
from plone.registry.interfaces import IRegistry
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from zope.formlib import form

class ControlPanel(ControlPanelForm):
    """ Diffbot API
    """
    form_fields = form.FormFields(IRelationsSettings)
    label = _(u"Relations Settings")
    description = _(u"Relations settings")
    form_name = _(u"Relations settings")

class ControlPanelAdapter(SchemaAdapterBase):
    """ Form adapter
    """
    implements(IRelationsSettings)

    def __init__(self, context):
        super(ControlPanelAdapter, self).__init__(context)
        self._settings = None

    @property
    def settings(self):
        """ Settings
        """
        if self._settings is None:
            self._settings = queryUtility(
                IRegistry).forInterface(IRelationsSettings, False)
        return self._settings

    @property
    def token(self):
        """ Get token
        """
        name = u"token"
        return getattr(self.settings, name, IRelationsSettings[name].default)

    @token.setter
    def token(self, value):
        """ Set token
        """
        self.settings.token = value

    @property
    def autoTagging(self):
        """ Enable auto-tagging
        """
        name = u"autoTagging"
        return getattr(self.settings, name, IRelationsSettings[name].default)

    @autoTagging.setter
    def autoTagging(self, value):
        """ Enable / disable auto-tagging
        """
        self.settings.autoTagging = value

    @property
    def autoTaggingFields(self):
        """ Fields
        """
        name = u"autoTaggingFields"
        return getattr(self.settings, name, IRelationsSettings[name].default)

    @autoTaggingFields.setter
    def autoTaggingFields(self, value):
        """ Update autoTaggingFields
        """
        self.settings.autoTaggingFields = value

    @property
    def autoTaggingLink(self):
        """ Link
        """
        name = u"autoTaggingLink"
        return getattr(self.settings, name, IIRelationsSettingsySettings[name].default)

    @autoTaggingLink.setter
    def autoTaggingLink(self, value):
        """ Update autoTaggingLink
        """
        self.settings.autoTaggingLink = value

    @property
    def autoTaggingBlackList(self):
        """ Blacklist
        """
        name = u"autoTaggingBlackList"
        return getattr(self.settings, name, IRelationsSettings[name].default)

    @autoTaggingBlackList.setter
    def autoTaggingBlackList(self, value):
        """ Update blacklist
        """
        self.settings.autoTaggingBlackList = value
