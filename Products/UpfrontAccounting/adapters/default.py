from zope.interface import implements
from Products.UpfrontAccounting.interfaces import IZeroMoneyInstance, \
    ICurrency
from Products.FinanceFields.Money import Money
from Products.Archetypes.interfaces import IFieldDefaultProvider
from DateTime import DateTime

class ZeroMoneyAdapter(object):

    implements(IFieldDefaultProvider, IZeroMoneyInstance)

    def __init__(self, context):
        self.context = context

    def __call__(self):
        currency = self.context.getAccountingCurrency()
        return Money('0.00', currency)


class NowAsDefaultDate(object):

    implements(IFieldDefaultProvider)

    def __init__(self, context):
        self.context = context

    def __call__(self):
        return DateTime()


class DefaultCurrencyAdapter(object):

    implements(IFieldDefaultProvider, ICurrency)

    def __init__(self, context):
        self.context = context

    def __call__(self):
        return self.context.getAccountingCurrency()
