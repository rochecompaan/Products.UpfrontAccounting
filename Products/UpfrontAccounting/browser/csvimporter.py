import csv
import time
from tempfile import mkstemp
from os import close, write, system
from cStringIO import StringIO

from zope.event import notify
from collective.progressbar.events import InitialiseProgressBar
from collective.progressbar.events import ProgressBar
from collective.progressbar.events import UpdateProgressEvent
from collective.progressbar.events import ProgressState

from Products.Five import BrowserView
from zope.interface import implements, Interface
from Products.CMFCore.utils  import getToolByName
from DateTime import DateTime


CSV_KEY = 'csv_file'
CSV_HEADERS_KEY = 'csv_headers'

class ICSVImporter(Interface):
    """ Marker interface
    """

class CSVImporter(BrowserView):
    """ Import a CSV file
    """

    implements(ICSVImporter)

    def __call__(self, *args, **kw):
        """ we render the template except when we are importing and
            writing progress to the response.
        """
        if self.request.has_key('import'):
            self.importfile()
        else:
            return self.index()

    def name(self):
        return self.__name__

    def update(self):
        if self.request.has_key(CSV_KEY):
            self.uploadfile()

    def uploadfile(self):
        """
        Read uploaded csv file and save it in sessions variable
        """
        session = self.request.SESSION
        csv_file = self.request.get(CSV_KEY, None)
        if csv_file is None:
            self._del_session_cache()
        else:
            session[CSV_KEY] = csv_file.read()

    def get_rows_sample(self):
        return self.get_rows()[1:10]

    def get_rows(self):
        """ Return all rows in the CSV file """
        csv_file_content = self.request.SESSION.get(CSV_KEY, '')
        return self._get_rows(csv_file_content)

    def _get_rows(self, content):
        dateformat = self.request.get('dateformat')
        delimiter = self.request.get('delimiter', 'comma')
        quote_char = self.request.get('quote_char', 'double_quote')
        encoding = self.request.get('encoding', 'utf-8')

        delim_map = {'tab':'\t', 'semicolon':';', 'colon':':', 'comma':',', 
                     'space':' ', 'asterisk': '*'}
        delimiter = delim_map[delimiter]
        quote_map = {'double_quote':'"', 'single_quote':"'", }
        quote_char = quote_map[quote_char]
        charset = self._site_encoding()

        # Workaround to get the buffer in U (universal line terminator) mode
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

        f = StringIO(buf.decode(encoding, 'replace').encode(charset))
        reader = csv.reader(f, delimiter=delimiter, lineterminator=chr(13))
        rows = []
        for row in reader:
            rows.append(row)
        return rows

    def get_headers(self):
        csvfile = self.request.SESSION.get(CSV_KEY)
        header_str = csvfile.split('\n')[0]
        return self._get_rows(header_str)[0]

    def importfile(self):
        """ Convert the uploaded csv data to content instances
        """
        view = self.context.restrictedTraverse('@@import-progress')
        bar = ProgressBar(self.context, self.request, 'Import', 'Import',
            view=view)
        notify(InitialiseProgressBar(bar))

        delimiter = self.request.get('delimiter', 'comma')
        quote_char = self.request.get('quote_char', 'double_quote')
        encoding = self.request.get('encoding', 'utf-8')

        delim_map = {'tab':'\t', 'semicolon':';', 'colon':':', 'comma':',', 
                     'space':' ', 'asterisk': '*'}
        delimiter = delim_map[delimiter]
        quote_map = {'double_quote':'"', 'single_quote':"'", }
        quote_char = quote_map[quote_char]
        charset = self._site_encoding()

        content = self.request.SESSION.get(CSV_KEY)
        lines = content.split('\n')
        f = StringIO(content.decode(encoding, 'replace').encode(charset))
        reader = csv.DictReader(f, delimiter=delimiter, lineterminator=chr(13))
        rows = []

        count = float(len(lines))
        progress = 0
        for index, row in enumerate(reader):
            self._addObject(row)

            progress = index / count * 100.0
            state = ProgressState(self.request, progress)
            notify(UpdateProgressEvent(state))

        state = ProgressState(self.request, 100)
        notify(UpdateProgressEvent(state))

        # delete file from session object as it can be several MB
        self._del_session_cache()

        
        ptool = getToolByName(self.context, 'plone_utils')
        ptool.addPortalMessage(u'Import successful')

        self.request.RESPONSE.write(
            '<script>document.location.href="%s</script>' %  
            self.context.absolute_url()
            )

    def _addObject(self, row):
        """ use row data from CSV file and create an object from it
        """
        content_type = self.request.get('content_type')
        if row.has_key('id'):
            new_id = row.get('id')
        else:
            new_id = self.context.generateUniqueId(type_name=content_type)
        self.context.invokeFactory(type_name=content_type, id=new_id)
        obj = self.context[new_id]

        # convert references to objects
        self._convert_references(row, obj)

        # split lines fields on comma
        islines = lambda x: x.type == 'lines'
        for field in obj.Schema().filterFields(islines):
            if row.has_key(field.getName()):
                value = row.get(field.getName())
                value = value.split(',')
                row[field.getName()] = value

        # convert boolean fields
        isboolean = lambda x: x.type == 'boolean'
        for field in obj.Schema().filterFields(isboolean):
            if row.has_key(field.getName()):
                value = row.get(field.getName())
                if value.lower() in ('true', 'yes', '1'):
                    value = True
                else:
                    value = False
                row[field.getName()] = value

        obj.edit(**row)

    def _del_session_cache(self):
        session = self.request.SESSION
        if session.has_key(CSV_KEY):
            del session[CSV_KEY]

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

    def _unique(self, dicts):
        "Removes duplicates from the import map."
        uniques = {}
        for dict_ in dicts:
            keys = dict_.keys()
            keys.sort()
            temp = []
            for key in keys:
                # stringify value in case we have an unhashable type
                val = str(dict_[key])
                temp.append((key, val))
            uniques[tuple(temp)] = dict_
        vals = uniques.values()
        return vals

    def _convert_references(self, row, obj):
        isreference = lambda x: x.type in ('reference', 'simplereference')
        for field in obj.Schema().filterFields(isreference):
            if row.has_key(field.getName()):
                value = row.get(field.getName())
                # is this a UID?
                rtool = getToolByName(self.context, 'reference_catalog')
                ref = rtool.lookupObject(value) 
                if ref is not None:
                    row[field.getName()] = ref
                    continue

                # or is this an unique id
                pc = getToolByName(self.context, 'portal_catalog')
                brains = pc(id=value)
                # if we find more than one we can't make any
                # assumptions
                if len(brains) == 1:
                    row[field.getName()] = brains[0].getObject()
                else:
                    del row[field.getName()]
