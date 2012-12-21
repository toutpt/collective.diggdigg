from zope import interface
from zope import schema


class Settings(interface.Interface):
    """addon settings"""

    buttons = schema.List(title=u"Buttons",
              value_type=schema.Choice(title=u"Button",
                        vocabulary="collective.diggdigg.vocabulary.buttons")
              )
