from email.Utils import formataddr
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email import Encoders

from zope.interface import implements
from zope.component import adapts
from DateTime import DateTime

from Products.UpfrontAccounting.interfaces import IMailInvoice, IMailStatement
from Products.UpfrontAccounting.content.interfaces import IInvoice, IAccount
from Products.CMFCore.utils import getToolByName
from Products.SecureMailHost.mail import Mail

class MailInvoice(object):

    implements(IMailInvoice)

    adapts(IInvoice)

    def __init__(self, invoice):
        self.invoice = invoice

    def send(self): 
        """ Send Invoice to recipients
        """
        invoice = self.invoice
        root = invoice.getAccountingRoot()
        portal = getToolByName(invoice, 'portal_url').getPortalObject()
        host = portal.MailHost
        template = getattr(portal, 'invoice_mail_template')
        encoding = portal.getProperty('email_charset')
        send_from_address = formataddr(
            ( root.getOrganisationName(), root.getEmail() )
        )

        # Compile a list of contacts for the customer
        customer = invoice.getCustomerAccount()
        to_addrs = []
        for contact in customer.getContacts():
            to_addrs.append(
                formataddr((contact.Title(), contact.getEmail()))
            )

        # if the customer doesn't have any contact, use the company
        # email address
        if not customer.getContacts():
            to_addrs.append(
                formataddr((customer.Title(), customer.getEmail()))
            )

        subject = '%s Invoice: %s' % (
            root.getOrganisationName(), invoice.getId())

        send_to_address = ', '.join(to_addrs)

        msg = MIMEMultipart('mixed')
        msg['Subject'] = subject
        msg['From'] = send_from_address
        msg['To'] = send_to_address

        # Generate message and attach to mail message
        message = template(OrganisationName=root.getOrganisationName())
        body = MIMEText(message, 'text', encoding)
        msg.attach(body)

        # Generate and attach PDF 
        invoice_pdf = invoice.invoice_pdf.getPDF(
            invoice.REQUEST, invoice.REQUEST.RESPONSE)
        pdf = MIMEBase('application', 'pdf')
        pdf.set_payload(invoice_pdf)

        # Encode the payload using Base64
        Encoders.encode_base64(pdf)

        # Set the filename parameter
        pdf.add_header('Content-Disposition', 'attachment',
            filename='%s.pdf' % invoice.getId())
        msg.attach(pdf)

        # We are not using SecureMailHost.secureSend because it cannot
        # handle a multipart message
        mail = Mail(send_from_address, send_to_address, msg,
            smtp_host=host.smtp_host, smtp_port=host.smtp_port,
            userid=host._smtp_userid, password=host._smtp_pass)
        mail.send()

        # Send the message to ourselves
        mail = Mail(send_from_address, send_from_address, msg,
            smtp_host=host.smtp_host, smtp_port=host.smtp_port,
            userid=host._smtp_userid, password=host._smtp_pass)
        mail.send()


class MailStatement(object):
    """ Mail a statement """

    implements(IMailStatement)

    adapts(IAccount)

    def __init__(self, account):
        self.account = account

    def send(self): 
        """ Send statement to recipients
        """
        account = self.account
        organisation = account.getAccountingRoot().getOrganisation()
        portal = getToolByName(account, 'portal_url').getPortalObject()
        host = portal.MailHost
        template = getattr(portal, 'statement_mail_template')
        encoding = portal.getProperty('email_charset')
        send_from_address = formataddr(
            ( organisation.Title(), organisation.getEmail() )
        )

        # Compile a list of contacts for the organisation
        customer = account.getOrganisation()
        to_addrs = []
        for contact in customer.getContacts():
            to_addrs.append(
                formataddr((contact.Title(), contact.getEmail()))
            )

        # if the customer doesn't have any contact, use the company
        # email address
        if not customer.getContacts():
            to_addrs.append(
                formataddr((customer.Title(), customer.getEmail()))
            )

        send_to_address = ', '.join(to_addrs)

        subject = '%s Statement: %s %s' % (organisation.Title(), 
            DateTime().Month(), DateTime().year() )

        msg = MIMEMultipart('mixed')
        msg['Subject'] = subject
        msg['From'] = send_from_address
        msg['To'] = send_to_address

        # Generate message and attach to mail message
        message = template(organisation=organisation)
        body = MIMEText(message, 'text', encoding)
        msg.attach(body)

        # Generate and attach PDF 
        statement_pdf = account.statement_pdf.getPDF(account.REQUEST,
            account.REQUEST.RESPONSE)
        pdf = MIMEBase('application', 'pdf')
        pdf.set_payload(statement_pdf)

        # Encode the payload using Base64
        Encoders.encode_base64(pdf)

        # Set the filename parameter
        pdf.add_header('Content-Disposition', 'attachment',
            filename='%s-statement-%s-%s.pdf' % (account.getId(),
            DateTime().Month(), DateTime().year()))
        msg.attach(pdf)

        # We are not using SecureMailHost.secureSend because it cannot
        # handle a multipart message
        mail = Mail(send_from_address, send_to_address, msg,
            smtp_host=host.smtp_host, smtp_port=host.smtp_port,
            userid=host._smtp_userid, password=host._smtp_pass)
        mail.send()

        # Resend it to ourselves
        mail = Mail(send_from_address, send_from_address, msg,
            smtp_host=host.smtp_host, smtp_port=host.smtp_port,
            userid=host._smtp_userid, password=host._smtp_pass)
        mail.send()
