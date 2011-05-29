from Products.Five import BrowserView

from Products.UpfrontAccounting.content.interfaces import IInvoice
from Products.UpfrontAccounting.interfaces import IMailInvoice, IMailStatement
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _

class MailObjects(BrowserView):
    def send_invoice_mail(self):
        """ Send a mail specific based on a content type - these are configured
            in adapters.zcml (eg MailInvoice)
        """
        IMailInvoice(self.context).send()

    def send_statement_mail(self):
        """ Send a mail specific based on a content type - these are configured
            in adapters.zcml (eg MailInvoice)
        """
        IMailStatement(self.context).send()

    def send_invoice_mails(self):
        """ Send mails adapted on a content type - these are configured
            in adapters.zcml (eg MailInvoice)
        """
        for path in self.request.get('paths', []):
            invoice = self.context.restrictedTraverse(path)
            IMailInvoice(invoice).send()

    def send_statement_mails(self):
        """ Send mails adapted on a content type - these are configured
            in adapters.zcml (eg MailInvoice)
        """
        for path in self.request.get('paths', []):
            account = self.context.restrictedTraverse(path)
            IMailStatement(account).send()

        self.context.plone_utils.addPortalMessage(
            _(u'Statements mailed successfully'))
        self.request.RESPONSE.redirect(self.context.absolute_url())

