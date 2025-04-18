import requests
import datetime
import csv  # Add this import at the top of the file
import json

cols = ["ListingKey", "ContractStatus", "ClosePrice", "ModificationTimestamp", 'SoldConditionalEntryTimestamp', 'SoldEntryTimestamp', 'ListAgentEmail']
# ListAgentDirectPhone Field
# ListAgentEmail Field
# BuyerAgentDirectPhone Field
# BuyerAgentEmail Field
# PurchaseContractDate
col_str = ",".join(cols)
print(col_str)
timestamp = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(weeks=1) 
formatted_timestamp = str(timestamp).replace(' ', 'T').split('.')[0] + "Z"
full_list = []
last_listing_key = None
while True:
    filters = [f"ModificationTimestamp ge {formatted_timestamp}", 
            "ListAgentFullName ne null",
            "ListAgentDirectPhone ne null"]
    # filters = ["ListingKey eq 'N12029818'"]
    if last_listing_key:
        filters.append(f"ListingKey gt '{last_listing_key}'")
    filter_str = " and ".join(filters)
    url = (
        "https://query.ampre.ca/odata/Property?"
        "$select="
        f"{col_str}"
        "&$filter="
        f"{filter_str}"
        "&$orderby=ListingKey"
        )

    payload = {}
    with open('headers_secret.json', 'r') as config_file:
        headers = json.load(config_file)
    print(url)
    response = requests.request("GET", url, headers=headers, data=payload)
    res_json = json.loads(response.text)["value"]
    if len(res_json) == 0:
        break
    full_list.extend(res_json)
    print(len(res_json))
    last_listing_key = res_json[-1]["ListingKey"]

print(len(res_json))
# print(json.dumps(full_list, indent=4))

# At the end of the script, after the while loop
csv_file_path = '/Users/noahchait/Documents/python tests/full_list.csv'
if full_list:
    keys = full_list[0].keys()  # Extract column names from the first dictionary
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=keys)
        writer.writeheader()  # Write the header row
        writer.writerows(full_list)  # Write the data rows

print(f"Data successfully written to {csv_file_path}")
