import csv
import time
from cStringIO import StringIO

from Products.Five import BrowserView
from zope.interface import implements, Interface
from Products.CMFCore.utils  import getToolByName
from DateTime import DateTime

from Products.UpfrontAccounting.config import \
        STATEMENT_CSV_KEY, STATEMENT_CSV_HEADERS_KEY
from Products.UpfrontAccounting.browser.utils import ListAccounts

class IImportStatement(Interface):
    """ Marker interface
    """

class ImportStatement(BrowserView):

    implements(IImportStatement)

    def update(self):
        if self.request.has_key(STATEMENT_CSV_KEY):
            self.uploadfile()
        elif self.request.has_key('import'):
            self.importstatement()

    def uploadfile(self):
        """
        Read uploaded csv file and save it in sessions variable
        """
        session = self.request.SESSION
        csv_file = self.request.get(STATEMENT_CSV_KEY, None)
        if csv_file is None:
            self._del_session_cache()
        else:
            if self.request.get('removeheader', 'no') != 'no':
                lines = csv_file.readlines()
                headers = ''.join(lines[0])
                session[STATEMENT_CSV_HEADERS_KEY] = headers
                content = ''.join(lines[1:])
            else:
                content = csv_file.read()
            session[STATEMENT_CSV_KEY] = content

    def get_rows_sample(self):
        return self.get_rows()[:10]

    def get_rows(self):
        """Don't import HectoMegaByte files, or you are asking for it!"""
        csv_file_content = self.request.SESSION.get(STATEMENT_CSV_KEY, '')
        return self._get_rows(csv_file_content)

    def _get_rows(self, content):
        dateformat = self.request.get('dateformat')
        fields_map = self.request.get('fields_map', {})
        delimiter = self.request.get('delimiter', 'comma')
        quote_char = self.request.get('quote_char', 'double_quote')
        encoding = self.request.get('encoding', 'latin-1')

        delim_map = {'tab':'\t', 'semicolon':';', 'colon':':', 'comma':',', 
                     'space':' ', 'asterisk': '*'}
        delimiter = delim_map[delimiter]
        quote_map = {'double_quote':'"', 'single_quote':"'", }
        quote_char = quote_map[quote_char]
        charset = self._site_encoding()


        # Workaround to get the buffer in U (universal line terminator) mode
        from tempfile import mkstemp
        from os import close, write, system
        # Write temp file
        fp, fname = mkstemp()
        try:
            write(fp, content)
        finally:
            close(fp)
        # Read temp file
        fh = open(fname, 'rU')
        try:
            buf = fh.read()
        finally:
            fh.close()
            system('rm "%s"' % fname)

        # This sucks! double memory usage
        f = StringIO(buf.decode(encoding, 'replace').encode(charset))
        reader = csv.reader(f, delimiter=delimiter, lineterminator=chr(13))
        rows = []
        for row in reader:
            if 'Date' in fields_map.values():
                for i, fieldname in fields_map.items():
                    if fieldname == 'Date':
                        break
                i = int(i)
                date = row[i]
                row[i] = self._format_date(date, dateformat)
            rows.append(row)
        return rows

    def get_headers(self):
        header_str = self.request.SESSION.get(STATEMENT_CSV_HEADERS_KEY, '')
        header_str = header_str.replace('Description', 'description')
        if header_str:
            return self._get_rows(header_str)[0]

    def capitalize(self, s):
        if not s: return s
        return "%s%s" % (s[0].upper(), s[1:])

    def headerSetLC(self):
        return [i.lower() for i in self.headerSet()]

    def headerSet(self):
        return ['Discard Field','Date','description','ReferenceNumber','Amount']

    def selectedIndex(self, headers, idx):
        if idx+1 >= len(headers):
            return 0
        lcset = self.headerSetLC()
        if headers[idx].lower() in lcset:
            return lcset.index(headers[idx].lower())
        return 0
            
    def importstatement(self):
        """Process the schema looking for data in the form"""
        cashbook = self.context
        pc = getToolByName(cashbook, 'portal_catalog')
        typestool = getToolByName(self.context, 'portal_types')
        items = []
        for key, value in self.request.form.items():
            if key.startswith('cashbookentry'):
                int_key = int(key.split('.')[-1])
                items.append((int_key, value.copy()))

        items.sort()
        account_title_map = self._account_title_map()

        for key, itemvalues in items:
            itemvalues = dict(itemvalues)

            if itemvalues['Account'] == '':
                continue

            # strip description
            desc = itemvalues.get('description').strip()
            phrases = cashbook.getStripPhrasesFromImport()
            for phrase in phrases:
                desc = desc.replace(phrase, '')
                desc = desc.strip()

            itemvalues['description'] = desc

            # look up account in uid_title_map
            account_title = itemvalues.get('Account')
            account = account_title_map.get(account_title)
            itemvalues['Account'] = account

            if account.getTaxIncludedInCashBookEntries():
                itemvalues['TaxIncluded'] = True

            if itemvalues.has_key('RememberDescription'):
                remember_text = itemvalues.get('RememberDescription')
                remember_text.strip()
                txt = account.getBankStatementText()
                txt = list(txt)
                if txt and txt[0] == '':
                    del txt[0]
                if remember_text not in txt:
                    txt.append(remember_text)
                    account.edit(BankStatementText=txt)

            item_id = cashbook.generateUniqueId(type_name='CashBookEntry')
            typestool.constructContent('CashBookEntry', cashbook.entries,
                item_id)

            item = cashbook.entries._getOb(item_id)

            amount = '%s %s' % \
                    (cashbook.getAccountingCurrency(), 
                     itemvalues.get('Amount', 0))
            itemvalues['Amount'] = amount

            # XXX: no validation yet
            item.edit(**dict(itemvalues))
            item.reindexObject()

        if self.request:
           self.request.RESPONSE.redirect(
                '%s/base_edit' % cashbook.entries.absolute_url()
            )

    def _account_title_map(self):
        view = ListAccounts(self.context, self.request)
        uidmap = {}
        for account in view.list():
            option = account.Title()
            uidmap[option] = account
        return uidmap

    def _del_session_cache(self):
        session = self.request.SESSION
        if session.has_key(STATEMENT_CSV_KEY):
            del session[STATEMENT_CSV_KEY]

    def _site_encoding(self):
        "Returns the site encoding"
        portal_properties = self.context.portal_properties
        site_props = portal_properties.site_properties
        return site_props.default_charset or 'utf-8'

    def _format_date(self, datestring, dateformat):
        """ Format date
                C = Century
                Y = Year
                M = Month
                D = Day
        """
        dateformat = dateformat.replace('CCYY', '%Y')
        dateformat = dateformat.replace('MM', '%m')
        dateformat = dateformat.replace('DD', '%d')
        return time.strftime('%Y-%m-%d',
            time.strptime(datestring, dateformat))

    def guess_account_descriptions(self, record, fields_map):
        """ Try to guess account from description on statement
        """
        if 'description' in fields_map.values():
            for i, fieldname in fields_map.items():
                if fieldname == 'description':
                    break
            i = int(i)
            statement_text = record[i]
        else:
            return '', ''

        statement_text = statement_text.strip()
        statement_text = statement_text.replace('(', '')
        statement_text = statement_text.replace(')', '')
        statement_text = statement_text.replace('"', '')
        statement_text = statement_text.replace("'", '')
        statement_text = statement_text.replace("-", ' ')

        pc = getToolByName(self.context, 'portal_catalog')
        account_types = ('Account', 'CustomerAccount', 'SupplierAccount')

        # 1. Query the getBankStatementText keyword index
        rs = pc(
            portal_type=account_types,
            getBankStatementText=statement_text
            )
        if rs:
            account = rs[0].getObject()
            return account.UID(), account.Title()

        # 2. Do an "AND" query on the BankStatementTextAsString text
        # index
        AND_statement_text = ' AND '.join(statement_text.split())
        rs = pc(
            portal_type=account_types,
            BankStatementTextAsString='%s' % AND_statement_text
            )
        if rs:
            account = rs[0].getObject()
            return account.UID(), account.Title()

        # 3. Do an "OR" query on the BankStatementTextAsString text
        # index
        rs = pc(
            portal_type=account_types,
            BankStatementTextAsString='%s' % statement_text
            )
        if rs:
            account = rs[0].getObject()
            return account.UID(), account.Title()

        # 4. Let's try and search on SearchableText too
        rs = pc(
            portal_type=account_types,
            SearchableText=statement_text
            )
        if rs:
            account = rs[0].getObject()
            return account.UID(), account.Title()

        return '', ''
