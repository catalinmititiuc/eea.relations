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
    def autoRelations(self):
        """ Enable auto-relations
        """
        name = u"autoRelations"
        return getattr(self.settings, name, IRelationsSettings[name].default)

    @autoRelations.setter
    def autoRelations(self, value):
        """ Enable / disable auto-relations
        """
        self.settings.autoRelations = value

    @property
    def autoRelationsFields(self):
        """ Fields
        """
        name = u"autoRelationsFields"
        return getattr(self.settings, name, IRelationsSettings[name].default)

    @autoRelationsFields.setter
    def autoRelationsFields(self, value):
        """ Update autoRelationsFields
        """
        self.settings.autoRelationsFields = value
