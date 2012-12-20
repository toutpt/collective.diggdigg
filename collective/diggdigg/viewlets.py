from zope import component
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.registry.interfaces import IRegistry
from collective.diggdigg.settings import Settings
from collective.diggdigg.ddclass import DIGGDIGG_CLASSES


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

    def get_buttons(self):
        url = self.context.absolute_url()
        title = self.context.Title()
        postId = self.context.getId()
        lazy = True

        registry = component.getUtility(IRegistry)
        settings = registry.forInterface(Settings)

        buttons = [button(self.context, self.request)\
                     for button in DIGGDIGG_CLASSES\
                       if button.NAME in settings.buttons]

        for button in buttons:
            button.constructURL(url, title,
                                button.getOptionButtonDesign(),
                                postId, lazy)
        return buttons
