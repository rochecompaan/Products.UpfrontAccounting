import logging
from Products.CMFCore.utils import getToolByName
from csvimporter import CSVImporter
from Products.UpfrontAccounting.content.TransactionEntry import \
    TransactionEntry

class TransactionImporter(CSVImporter):
    """ Specialise CSVImporter to import transaction csv files
    """

    def _addObject(self, row):
        """ use row data from CSV file and create an object from it
        """
        if row.has_key('id'):
            txn_id = row.get('id')

            # increment transaction id
            prefix = self.context.getLedger().getTransactionPrefix()
            txn_number = int(txn_id.replace(prefix, ''))
            if self.context.getLedger().getTransactionID() < txn_number:
                self.context.getLedger().setTransactionID(txn_number)

        else:
            txn_id = self.context.generateUniqueId(type_name='Transaction')

        # create transaction if it doesn't exist
        if not self.context.hasObject(txn_id):
            self.context.invokeFactory(type_name='Transaction', id=txn_id,
                title=row['title'], effectiveDate=row['effectiveDate'])

        txn = self.context[txn_id]

        # lookup account
        pc = getToolByName(self.context, 'portal_catalog')
        brains = pc(id=row['Account'])
        __traceback_info__ = str(row)
        assert len(brains) == 1
        row['Account'] = brains[0].getObject()

        # create transaction entry
        entry_id = txn.generateUniqueId('TransactionEntry')
        entry = TransactionEntry(entry_id)
        txn._setObject(entry_id, entry)
        entry = txn._getOb(entry_id)

        row['id'] = entry_id
        entry.edit(**row)

