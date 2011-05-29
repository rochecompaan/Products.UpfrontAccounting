import logging
from Products.CMFCore.utils import getToolByName
from csvimporter import CSVImporter
from Products.UpfrontAccounting.content.CashBookEntry import \
    CashBookEntry

class CashBookImporter(CSVImporter):
    """ Specialise CSVImporter to import cashbook csv files
    """

    def _addObject(self, row):
        """ use row data from CSV file and create an object from it
        """
        entryfolder = self.context.entries
        if row.has_key('id'):
            new_id = row.get('id')
        else:
            new_id = entryfolder.generateUniqueId(type_name='CashBookEntry')
        portal_types = getToolByName(entryfolder, 'portal_types')
        portal_types.constructContent('CashBookEntry', entryfolder, new_id)
        entry = entryfolder[new_id]

        # convert references to objects
        self._convert_references(row, entry)

        entry.edit(**row)

