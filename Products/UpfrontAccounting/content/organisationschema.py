from Products.Archetypes.public import *
from Products.UpfrontAccounting.config import BANK_ACCOUNT_TYPES, COUNTRY_NAMES

organisation_schema = Schema((
    StringField('OrganisationName',
        required=1,
        searchable='1',
        widget=StringWidget(
            label='Organisation Name',
            label_msgid='label_organisationname',
        ),
    ),
    StringField('RegistrationNumber',
        widget=StringWidget(
            label='Registration Number',
            label_msgid='label_registrationnumber',
        ),
    ),
    StringField('TaxNumber',
        widget=StringWidget(
            label='Tax Number',
            label_msgid='label_taxnumber',
        ),
    ),
    StringField('Phone',
        index='FieldIndex:brains',
        widget=StringWidget(
            label='Phone Number',
            label_msgid='label_phone',
        ),
    ),
    StringField('Fax',
        index='FieldIndex:brains',
        widget=StringWidget(
            label='Fax Number',
            label_msgid='label_fax',
        ),
    ),
    ImageField('Logo'),
    StringField('Email',
        schemata='Address',
        widget=StringWidget(
            label='Organisation email address',
            label_msgid='label_emailaddress'
        ),
        validators=('isEmail',)
    ),
    TextField('Address',
        schemata='Address',
        widget=TextAreaWidget(
           label_msgid='label_address',
        ),
    ),
    StringField('City',
        schemata='Address',
        widget=StringWidget(
           label_msgid='label_city',
        ),
    ),
    StringField('PostalCode',
        schemata='Address',
        widget=StringWidget(
           label='Postal Code',
           label_msgid='label_postalcode',
        ),
    ),
    StringField('State',
        schemata='Address',
        widget=StringWidget(
           label='State/Province',
           label_msgid='label_stateprovince',
        ),
    ),
    StringField('Country',
        schemata='Address',
        vocabulary=COUNTRY_NAMES,
        widget=SelectionWidget(
           label='Country',
           label_msgid='label_country',
        ),
    ),
    StringField('BankAccountType',
        schemata='Bank',
        vocabulary=BANK_ACCOUNT_TYPES,
        widget=SelectionWidget(
            label='Type of account', 
            label_msgid='label_accounttype',
        ),
    ),
    StringField('BankAccountName',
        schemata='Bank',
        widget=StringWidget(
            label='Account name',
            label_msgid='label_accountname',
        ),
    ),
    StringField('BankAccountNumber',
        schemata='Bank',
        widget=StringWidget(
            label='Account number',
            label_msgid='label_accountnumber',
        ),
    ),
    StringField('BankBranchCode',
        schemata='Bank',
        widget=StringWidget(
            label='Branch code',
            label_msgid='label_branchcode',
        ),
    ),
    StringField('BankName',
        schemata='Bank',
        widget=StringWidget(
            label='Bank name',
            label_msgid='label_bankname',
        ),
    ),
    StringField('BankSwiftCode',
        schemata='Bank',
        widget=StringWidget(
            label='Swift banking code',
            label_msgid='label_swift_banking_code',
        ),
    ),
),
)

