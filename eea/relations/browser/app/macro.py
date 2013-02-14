""" View macro utils
"""
from Products.Five.browser import BrowserView
from eea.relations.component import getForwardRelationWith
from eea.relations.component import getBackwardRelationWith
from Products.CMFCore.utils import getToolByName


class Macro(BrowserView):
    """ Categorize relations
    """

    def checkPermission(self, doc):
        """ Check document permission
        """
        mtool = getToolByName(self.context, 'portal_membership')
        if mtool.checkPermission('View', doc):
            return doc
        return None

    def forward(self, **kwargs):
        """ Return forward relations by category
        """
        tabs = {}

        fieldname = kwargs.get('fieldname', 'relatedItems')
        field = self.context.getField(fieldname)
        if not field:
            return tabs

        accessor = field.getAccessor(self.context)
        #getRelatedItems = getattr(self.context, 'getRelatedItems', None)

        relations = accessor()
        for relation in relations:
            if not self.checkPermission(relation):
                continue

            forward = getForwardRelationWith(self.context, relation)
            if not forward:
                continue

            name = forward.getField('forward_label').getAccessor(forward)()
            if name not in tabs:
                tabs[name] = []
            tabs[name].append(relation)
        tabs = tabs.items()
        tabs.sort()
        return tabs

    def backward(self, **kwargs):
        """ Return backward relations by category
        """
        tabs = {}
        getBRefs = getattr(self.context, 'getBRefs', None)
        if not getBRefs:
            return tabs

        relation = kwargs.get('relation', 'relatesTo')

        relations = getBRefs(relation)
        contentTypes = {}
        nonBackwardRelations = []
        if relations:
            # save the name and the portal type of the first relation that we
            # have permission to use.
            # this way we can check if other relations are of same portal_type
            # if they are then we don't need to check if it's a backward
            # relation and what is it's name, we can just add it to the tabs
            # for that relation name the relation item
            for relation in relations:
                if self.checkPermission(relation):
                    firstRelation = relation
                    backward = getBackwardRelationWith(self.context,
                                                                  firstRelation)
                    if not backward:
                        return tabs
                    name = backward.getField('backward_label').getAccessor(
                                                                     backward)()
                    # save for the portal_type the resulted backwards
                    # relation name
                    contentTypes[firstRelation.portal_type] = name
                    break

        for relation in relations:
            if not self.checkPermission(relation):
                continue
            portalType = relation.portal_type
            # if the portal_type of the relation is not already in
            # contentTypes than we are dealing with a backward relation that
            # is different from the ones we had before therefore we need
            if portalType not in contentTypes:
                # don't check if relation is backward if the portal_type has
                # already been identified as nonBackward
                if portalType in nonBackwardRelations:
                    continue
                backward = getBackwardRelationWith(self.context, relation)
                if not backward:
                    nonBackwardRelations.append(portalType)
                    continue
                name = backward.getField('backward_label').getAccessor(backward)()
                contentTypes[portalType] = name
            name = contentTypes[portalType]

            if name not in tabs:
                tabs[name] = []
            tabs[name].append(relation)
        tabs = tabs.items()
        tabs.sort()
        return tabs
