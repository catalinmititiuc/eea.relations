import logging
from Products.Five.browser import BrowserView
from eea.relations.component import queryForwardRelations
from Products.CMFCore.utils import getToolByName

logger = logging.getLogger('eea.relations.browser.popup')

class Popup(BrowserView):
    """ Widget popup helper
    """
    _relations = []
    _field = ''
    _uids = ()

    @property
    def field(self):
        return self._field

    @property
    def uids(self):
        return self._uids

    @property
    def relations(self):
        if self._relations:
            return self._relations
        self._relations = queryForwardRelations(self.context)
        return self._relations

    def tabs(self):
        """ Return popup tabs
        """
        rtool = getToolByName(self.context, 'portal_relations')
        for relation in self.relations:
            nto = relation.getField('to').getAccessor(relation)()
            if nto not in rtool.objectIds():
                continue

            required = relation.getField('required').getAccessor(relation)()
            yield rtool[nto], required

    def __call__(self, **kwargs):
        if self.request:
            kwargs.update(self.request.form)
        field = kwargs.get('field', '')
        if field:
            self._field = field

        # Uids
        uids = kwargs.get('uids', ())
        self._uids = uids

        return self.index()

class BaseView(BrowserView):
    """ Base view for selected item
    """
    _field = ''
    _mode = 'view'
    _uids = ()

    @property
    def field(self):
        return self._field

    @property
    def mode(self):
        return self._mode

    @property
    def uids(self):
        return self._uids

    def setup(self, **kwargs):
        """ Setup view
        """
        if self.request:
            kwargs.update(self.request.form)

        # Set mode
        mode = kwargs.get('mode', 'view')
        self._mode = mode

        # Set field
        field = kwargs.get('field', '')
        self._field = field

        # Set uids
        uids = kwargs.get('uids', ())
        if not isinstance(uids, (list, tuple)):
            uids = uids,
        self._uids = [uid for uid in uids if uid]

class PopupSelectedItems(BaseView):
    """ Widget popup selected items helper
    """
    @property
    def items(self):
        """ Return selected items
        """
        if not self.uids:
            raise StopIteration

        ctool = getToolByName(self.context, 'portal_catalog')
        for uid in self.uids:
            if not uid:
                continue
            brains = ctool(UID=uid)
            for brain in brains:
                yield brain.getObject()

    def __call__(self, **kwargs):
        """ Render
        """
        self.setup(**kwargs)
        return self.index()

class PopupSelectedItem(BaseView):
    """ Display an item
    """
    def __call__(self, **kwargs):
        self.setup(**kwargs)
        return self.index()
