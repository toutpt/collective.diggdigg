from zope import component
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.registry.interfaces import IRegistry
from collective.diggdigg.settings import Settings
from collective.diggdigg.buttons.button import IButton, cmp_button


class DiggDigg(ViewletBase):
    """DiggDigg base viewlet"""
    index = ViewPageTemplateFile("diggdigg.pt")

    def render(self):
        if self.available:
            self.update()
            return self.index()

    @property
    def available(self):
        #TODO: push types over portal_registry
        return self.context.portal_type in ('Document', 'Event', 'News Item')

    def update(self):
        ViewletBase.update(self)
        buttons = list(component.getAdapters((self.context, self.request),
                                             IButton))
        registry = component.getUtility(IRegistry)
        settings = registry.forInterface(Settings)

        self.buttons = [button for name, button in buttons\
                        if button.NAME in settings.buttons]

        self.buttons.sort(cmp=cmp_button)

    def get_globalsettings(self):
        return "var dd_offset_from_content = 51;\
                var dd_top_offset_from_content = 51;"
