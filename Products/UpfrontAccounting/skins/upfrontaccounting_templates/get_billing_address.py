## Script (Python) "get_billing_address"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=org, innerJoin=None, outerJoin=None
##title=
##
""" Compute the billing address for a quote or invoice
"""
fields = []

for fieldName in ('Address', 'City', 'PostalCode', 'Country'):
    field = org.Schema().get(fieldName)
    accessor = field.getAccessor(org)
    value = accessor()
    if value:
        fields.append(value)

return outerJoin.join(fields)
