from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class DiggDigg(ViewletBase):
    """DiggDigg base viewlet"""
    index = ViewPageTemplateFile("diggdigg.pt")

    def update(self):
        ViewletBase.update(self)

    def render(self):
        if self.available:
            return self.index()

    @property
    def available(self):
        #TODO: push types over portal_registry
        return self.context.portal_type in ('Document', 'Event', 'News Item')
