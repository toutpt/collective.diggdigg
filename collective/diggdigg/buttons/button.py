import logging
from zope import component
from zope import interface
from zope import schema
from plone.registry.interfaces import IRegistry
from Products.Archetypes.interfaces.base import IBaseObject
from zope.publisher.interfaces import IRequest


logger = logging.getLogger("collective.diggdigg")


class IButton(interface.Interface):
    """a digg digg button"""
    weight = schema.Int(title=u"Weight")
    id = schema.ASCIILine(title=u"ID")


class Button(object):
    """base button"""
    interface.implements(IButton)
    component.adapts(IBaseObject, IRequest)
    settings_keys = []
    registry_key = ""
    id = "button"

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        self.update()
        self.initialize_attributes()
        return self.index()

    def update(self):
        self.portal_state = component.getMultiAdapter((self.context,
                                                       self.request),
                                                  name="plone_portal_state")
        self.portal_registry = component.getUtility(IRegistry)
        self.weight = self.portal_registry.get(self.registry_key + 'weight',
                                               100)

    def initialize_attributes(self):
        for key in self.settings_keys:
            value = getattr(self, key, None)
            rvalue = self.portal_registry.get(self.registry_key + key, '')
            if value is None or value != rvalue and rvalue:
                setattr(self, key, rvalue)

    def log(self, message):
        logger.info(message)


def cmp_button(b1, b2):
    if b1.weight < b2.weight:
        return -1
    elif b1.weight > b2.weight:
        return 1
    if b1.id < b2.id:
        return -1
    elif b1.id > b2.id:
        return 1
    return 0
