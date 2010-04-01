from zope import interface
from eea.facetednavigation.interfaces import IFacetedNavigable
from p4a.subtyper.interfaces import IPortalTypedFolderishDescriptor

class EEARelationsContentTypeDescriptor(object):
    """ Abstract report descriptor
    """
    interface.implements(IPortalTypedFolderishDescriptor)
    title = u'Faceted Navigable'
    description = u'Faceted navigable'
    type_interface = IFacetedNavigable
    for_portal_type = 'EEARelationsContentType'
