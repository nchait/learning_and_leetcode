import json
print("hello")
f = open('/Users/noahchait/Documents/python tests/learning_and_leetcode/test.json')
dct = json.load(f)
fields = [field["FieldName"] for field in dct['value']]
print(len(fields))
price_fields=[field for field in fields if "listagent" in field.lower()]
print(len(price_fields))
print(price_fields)
# ['ClosePrice', 'ClosePriceHold', 'ListPrice', 'ListPriceUnit', 'OriginalListPrice', 
# 'OriginalListPriceUnit', 'PercentListPrice', 'PreviousListPrice', 'PriceChangeTimestamp', 
# 'PriorPriceCode', 'PriorPriceCodeStatus', 'Year1LeasePrice', 'Year1LeasePriceHold', 
# 'Year2LeasePrice', 'Year2LeasePriceHold', 'Year3LeasePrice', 'Year3LeasePriceHold', 
# 'Year4LeasePrice', 'Year4LeasePriceHold', 'Year5LeasePrice', 'Year5LeasePriceHold']
# ClosePrice

# ['AddChangeTimestamp', 'BackOnMarketEntryTimestamp', 'DealFellThroughEntryTimestamp', 'DocumentsChangeTimestamp', 'ExtensionEntryTimestamp', 'ImportTimestamp', 'LeasedConditionalEntryTimestamp', 'LeasedEntryTimestamp', 'MajorChangeTimestamp', 'MediaChangeTimestamp', 'ModificationTimestamp', 'NumberOfFullTimeEmployees', 'OpenHouseEndTime', 'OpenHouseStartTime', 'OriginalEntryTimestamp', 'PhotosChangeTimestamp', 'PriceChangeTimestamp', 'SoldConditionalEntryTimestamp', 'SoldEntryTimestamp', 'SuspendedEntryTimestamp', 'SystemModificationTimestamp', 'TerminatedEntryTimestamp', 'TimestampSQL']
# 'SoldConditionalEntryTimestamp', 'SoldEntryTimestamp', 'ModificationTimestamp'

