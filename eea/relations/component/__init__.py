""" Components
"""
import logging
from zope.component import queryAdapter
from eea.relations.interfaces import IContentType
from eea.relations.component.interfaces import IContentTypeLookUp
from eea.relations.component.interfaces import IRelationsLookUp

logger = logging.getLogger('eea.relations.queryContentType')

def queryContentType(context, perform_extended_search=False):
    """ Lookup for context related content-type in portal_relations
    """
    connecter = queryAdapter(context, IContentTypeLookUp)
    if not connecter:
        logger.exception('No IContentTypeLookUp adapter found for '
                         '%s', context)
        return None
    return connecter(perform_extended_search)

def queryForwardRelations(context):
    """ Lookup for context possible forward relations
    """
    if not IContentType.providedBy(context):
        context = queryContentType(context)
    if not context:
        return
    connecter = queryAdapter(context, IRelationsLookUp)
    if not connecter:
        logger.exception('No IRelationsLookUp adapter found for '
                         '%s', context)
        return
    for relation in connecter.forward():
        yield relation

def queryBackwardRelations(context):
    """ Lookup for context possible backward relations
    """
    if not IContentType.providedBy(context):
        context = queryContentType(context)
    if not context:
        return
    connecter = queryAdapter(context, IRelationsLookUp)
    if not connecter:
        logger.exception('No IRelationsLookUp adapter found for '
                         '%s', context)
        return
    for relation in connecter.backward():
        yield relation

def getForwardRelationWith(context, ctype,
                           perform_extended_search=False):
    """ Get forward relation with ctype

    Returns None if I can't find possible relation or
    possible relation object from portal_relations
    """
    if not IContentType.providedBy(context):
        context = queryContentType(context)
    if not context:
        return None
    new_ctype = ctype
    if not IContentType.providedBy(ctype):
        new_ctype = queryContentType(ctype)
    if not new_ctype:
        return None

    connecter = queryAdapter(context, IRelationsLookUp)
    if not connecter:
        logger.exception('No IRelationsLookUp adapter found for '
                         '%s', context)
        return None
    result = connecter.forward_with(new_ctype)
    if not result and perform_extended_search:
        relations = queryContentType(ctype, perform_extended_search=True)
        for relation in relations:
            check = connecter.forward_with(relation)
            if not check:
                continue
            return check
    else:
        return result

def getBackwardRelationWith(context, ctype):
    """ Get backward relation with ctype

    Returns None if I can't find possible relation or
    possible relation object from portal_relations
    """
    if not IContentType.providedBy(context):
        context = queryContentType(context)
    if not context:
        return None

    if not IContentType.providedBy(ctype):
        ctype = queryContentType(ctype)
    if not ctype:
        return None

    connecter = queryAdapter(context, IRelationsLookUp)
    if not connecter:
        logger.exception('No IRelationsLookUp adapter found for '
                         '%s', context)
        return None
    return connecter.backward_with(ctype)
