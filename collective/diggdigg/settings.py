from zope import interface
from zope import schema
from collective.diggdigg.ddclass import DiggDiggVocabulary


class Settings(interface.Interface):
    """addon settings"""

    buttons = schema.List(title=u"Buttons",
                          value_type=schema.Choice(title=u"Button",
                                        vocabulary=DiggDiggVocabulary))
