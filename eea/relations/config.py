""" Config
"""
from eea.relations import graph
GRAPHVIZ_PATHS = graph.GRAPHVIZ_PATHS
PROJECTNAME = 'eea.relations'
ADD_CONTENT_PERMISSION = "Add portal content"

from zope.i18nmessageid.message import MessageFactory
EEAMessageFactory = MessageFactory('eea')
