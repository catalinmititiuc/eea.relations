""" Interfaces
"""
from zope.interface import Interface
from zope import schema
from eea.relations.config import EEAMessageFactory as _

class IRelationsSettings(Interface):
    """ Alchemy settings
    """
    autoRelations = schema.Bool(
        title=_(u'Enable auto-relations'),
        description=_(u"Lookup internal links within object content and "
                      "automatically update related items"),
        required=False,
        default=False
    )

    autoRelationsFields = schema.List(
        title=_(u"Lookup fields"),
        description=_(u"Lookup these fields for internal links"),
        required=True,
        default=[u'text', u'body'],
        value_type=schema.TextLine()
    )
