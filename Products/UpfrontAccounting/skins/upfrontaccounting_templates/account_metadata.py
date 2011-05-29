## Script (Python) "account_metadata"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
''' return a list of tuples containing
        category, account number, account name, account type
'''

return (
#Financial Category : B15 - Retained Income
('B15', '520/000', 'Retained Income / (Accumulated Loss)', 'Asset'),
('B15', '530/000', 'Shareholder Loans', 'Asset'),

#Financial Category : B25 - Long Term Borrowings
('B25', '550/000', 'Long Term Liabilities', 'Liability'),

#Financial Category : B35 - Fixed Assets
('B35', '610/000', 'Land & Buildings', 'Asset'),
('B35', '620/000', 'Motor Vehicles', 'Asset'),
('B35', '625/000', 'Computer Equipment', 'Asset'),
('B35', '626/000', 'Computer Software', 'Asset'),
('B35', '630/000', 'Office Equipment', 'Asset'),
('B35', '635/000', 'Furniture & Fittings', 'Asset'),
('B35', '660/000', 'Other Fixed Assets', 'Asset'),

#Financial Category : B40 - Investments
('B40', '710/000', 'Investments', 'Asset'),

#Financial Category : B45 - Other Fixed Assets
('B45', '700/000', 'Goodwill / Intangible Assets', 'Asset'),

#Financial Category : B50 - Inventory
('B50', '770/000', 'Inventory', 'Asset'),

#Financial Category : B55 - Accounts Receivable
('B55', '800/000', 'Accounts Receivable', 'Asset'),

#Financial Category : B60 - Bank
('B60', '840/000', 'Cheque Account', 'Asset'),
('B60', '845/000', 'Petty Cash', 'Asset'),

#Financial Category : B65 - Other Current Assets
('B65', '810/000', 'POS Cash Control', 'Asset'),
('B65', '820/000', 'Sundry Customers', 'Asset'),

#Financial Category : B70 - Accounts Payable
('B70', '900/000', 'Accounts Payable', 'Liability'),

#Financial Category : B80 - Other Current Liabilities
('B80', '920/000', 'Sundry Suppliers', 'Liability'),
('B80', '940/000', 'Provision for Future Expenses', 'Liability'),
('B80', '940/010', 'Provision for Insurance', 'Liability'),
('B80', '940/020', 'Provision for Salary Bonus', 'Liability'),
('B80', '950/000', 'Sales Tax Control Account', 'Liability'),
('B80', '951/000', 'Sales tax Provision Account', 'Liability'),
('B80', '960/000', 'Credit Card', 'Liability'),
('B80', '999/000', 'Opening Balance / Suspense Account', 'Liability'),

#Financial Category : I10 - Sales
('I10', '100/000', 'Sales', 'Income'),

#Financial Category : I15 - Cost of Sales
('I15', '200/000', 'Cost of Sales / Purchases', 'Expense'),

#Financial Category : I20 - Other Income
('I20', '275/000', 'Interest Received', 'Income'),
('I20', '280/000', 'Pft/Loss on Sale of Non Current Assets', 'Income'),
('I20', '285/000', 'Bad Debts Recovered', 'Income'),
('I20', '290/000', 'Sundry Income', 'Income'),

#Financial Category : I25 - Expenses
('I25', '300/000', 'Accounting Fees', 'Expense'),
('I25', '305/000', 'Advertising & Promotions', 'Expense'),
('I25', '315/000', 'Bad Debts', 'Expense'),
('I25', '320/000', 'Bank Charges', 'Expense'),
('I25', '325/000', 'Cleaning', 'Expense'),
('I25', '330/000', 'Computer Expenses', 'Expense'),
('I25', '335/000', 'Consulting Fees', 'Expense'),
('I25', '340/000', 'Courier & Postage', 'Expense'),
('I25', '345/000', 'Depreciation', 'Expense'),
('I25', '355/000', 'Discount Allowed for Cash', 'Expense'),
('I25', '360/000', 'Donations', 'Expense'),
('I25', '365/000', 'Electricity & Water', 'Expense'),
('I25', '370/000', 'Entertainment Expenses', 'Expense'),
('I25', '375/000', 'Finance Charges', 'Expense'),
('I25', '380/000', 'General Expenses', 'Expense'),
('I25', '385/000', 'Insurance', 'Expense'),
('I25', '390/000', 'Interest Paid', 'Expense'),
('I25', '395/000', 'Leasing Charges', 'Expense'),
('I25', '400/000', 'Legal Fees', 'Expense'),
('I25', '405/000', 'Levies', 'Expense'),
('I25', '415/000', 'Motor Vehicle Expenses', 'Expense'),
('I25', '420/000', 'Printing & Stationery', 'Expense'),
('I25', '430/000', 'Rent Paid', 'Expense'),
('I25', '435/000', 'Repairs & Maintenance', 'Expense'),
('I25', '440/000', 'Salaries & Wages', 'Expense'),
('I25', '445/000', 'Staff Training', 'Expense'),
('I25', '450/000', 'Staff Welfare', 'Expense'),
('I25', '450/010', 'Medical Aid', 'Expense'),
('I25', '455/000', 'Subscriptions', 'Expense'),
('I25', '456/000', 'Memberships', 'Expense'),
('I25', '460/000', 'Telephone & Fax', 'Expense'),
('I25', '465/000', 'Travel & Accommodation', 'Expense'),
('I25', '470/000', 'Subcontractors', 'Expense'),
('I25', '480/000', 'Income Tax', 'Expense'),
)
