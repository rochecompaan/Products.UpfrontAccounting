from zope.interface import implements, Interface
from Products.Five import BrowserView
from DateTime import DateTime
from Products.UpfrontAccounting.interfaces import ICSVWriter

class ICSVExporter(Interface):
    """ Marker interface
    """

class CSVExporter(BrowserView):
    """ Export a CSV file
    """

    implements(ICSVExporter)

    def __call__(self):
        """ Lookup CSVWriter for context and return CSV file """
        writer = ICSVWriter(self.context)
        output = writer.write()

        filename = '%s.csv' % self.context.getId()

        output.seek(0)
        output = output.read()
        request = self.request
        request.RESPONSE.setHeader('Content-Type', 
            'text/comma-separated-values; charset=utf-8')
        request.RESPONSE.setHeader('Content-Disposition',
            'attachment; filename=%s' % filename)
        request.RESPONSE.setHeader('Content-Length', len(output))
        request.RESPONSE.setHeader('Cache-Control', 's-maxage=0')

        return output


