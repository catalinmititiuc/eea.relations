""" Widget
"""
from Products.Archetypes.atapi import registerType
from Products.Archetypes.Registry import registerWidget
from eea.relations.config import PROJECTNAME
from referencewidget import EEAReferenceBrowserWidget
from referencedemo import EEARefBrowserDemo

registerWidget(EEAReferenceBrowserWidget,
    title='EEA Reference Browser',
    description=(('Reference widget that allows you to browse '
                  'or search the portal for objects to refer to.')),
    used_for=('Products.Archetypes.Field.ReferenceField',))

registerType(EEARefBrowserDemo, PROJECTNAME)
