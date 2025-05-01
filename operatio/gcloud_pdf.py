from google.cloud import storage
import PyPDF2
import re
import json
import csv
import os
import logging
import requests
import datetime

def get_address(data):
    first_line = data.split('\n')[0]
    return first_line.strip()

def read_pdf(file_path):
    try:
        # Open the PDF file in read-binary mode
        with open(file_path, 'rb') as pdf_file:
            # Create a PDF reader object
            reader = PyPDF2.PdfReader(pdf_file)
            
            # Extract text from each page
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            
            return text
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_numbers(line, is_coop):
    if line == "":
        return []
    output = []
    sections = line.split(" | ")
    name_and_role = sections[0]
    if ", " in name_and_role:
        split_name_and_role = name_and_role.split(", ")
        if len(split_name_and_role) >= 2:
            logging.warning(f"Unexpected format in name_and_role: {name_and_role}")
        name = split_name_and_role[0].strip()
        role = split_name_and_role[-1].strip()
    else:
        name = name_and_role.strip()
        role = "LISTED"
    if is_coop:
        role += " (CO-OP)"
    if name == "MEMBER NON-PROPTX":
        name = "UNKNOWN PERSON"
    elif name == "NON-PROPTX BOARD OFFICE":
        name = "UNKNOWN OFFICE"
    if len(sections) == 1:
        return [(name, "", "", role)]
    numbers = sections[1:]
    print("Numbers: ", numbers)
    for number in numbers:
        number = number.strip()
        if number.startswith("PHONE:"):
            number_type = "PHONE"
            number = number.replace("PHONE:", "").strip()
        elif number.startswith("FAX:"):
            number_type = "FAX"
            number = number.replace("FAX:", "").strip()
        elif number.startswith("LISTED:"):
            number_type = "LISTED"
            number = number.replace("LISTED:", "").strip()
        else:
            continue
        output.append((name, number_type, number, role))
    return output
# [("name", "type", "123-456-7890", "Salesperson"), ("name", "type", "123-456-7890", "Salesperson")]

def cleanup_numbers(data):
    numbers_str = data.split('LISTING CONTRACTED WITH\n')[1]
    numbers_str = numbers_str.replace('CO-OP', '                  \nCO-OP')
    page_end = numbers_str.find('Prepared By:')
    if page_end != -1:
        block = numbers_str[page_end: page_end + 233]
        numbers_str = numbers_str.replace(block, 'PAGE ENDS HERE')
    numbers_str = numbers_str.replace('\n \n', '\n').replace('\nPHONE\n', ' | PHONE: ').replace('\nFAX\n', ' | FAX: ')
    other_numbers = re.findall(r"\n\d{3}-\d{3}-\d{4}", numbers_str)
    for other_number in other_numbers:
        numbers_str = numbers_str.replace(other_number, " | LISTED: " + other_number[1:])
    number_str_lines = numbers_str.split('\n')
    cleaned_lines = [number_str_lines[0]] + [line.strip() for line in number_str_lines[1:] if ',' in line.strip() or 'CO-OP' in line]
    print(f"Numbers String: {numbers_str}")
    return '\n'.join(cleaned_lines)

def get_phone_numbers(data):
    cleaned_data = cleanup_numbers(data)
    # print(f"Cleaned Data:{cleaned_data}")
    # print(cleaned_data)
    output = []
    if 'CO-OP' in cleaned_data:
        non_coop_section, coop_section = cleaned_data.split('CO-OP\n')
        for non_coop_line in non_coop_section.split('\n'):
            output += get_numbers(non_coop_line, False)
        for coop_line in coop_section.split('\n'):
            output += get_numbers(coop_line, True)
    else:
        for non_coop_line in cleaned_data.split('\n'):
            output += get_numbers(non_coop_line, False)
    return output

def get_price(data):
    regex = r"DOM\nSOLD\n\$(\d{1,3}(?:,\d{3})*)\s*\nTAXES"
    matches = re.findall(regex, data)
    assert len(matches) == 1, f"Expected 1 match, found {len(matches)}"
    return matches[0]

def output_csv(mappings, file_name):
    # Write the mapping to a CSV file
    csv_file_path = "/Users/noahchait/Documents/python tests/learning_and_leetcode/operatio/csvs/" + file_name.replace('.pdf', ".csv")
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['listing', 'name_or_office', 'role', 'number_type', 'number', 'price']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        # Write the header and rows
        writer.writeheader()
        writer.writerows(mappings)

    print(f"Mapping has been written to {csv_file_path}")

def output_json(mappings, file_name):
    for i in range(len(mappings)):
        # URL to send the JSON data
        url = "https://www.zohoapis.com/crm/v7/functions/webhook_to_catch_lead_info/actions/execute"
        params = {
            "auth_type": "apikey",
            "zapikey": "1003.a332aaf6b2bc38c8994708f4b84b8fc0.648090912fb33539fa959ed603ff26a7"
        }

        # Send the JSON data as a POST request
        response = requests.post(url, params=params, json=mappings[i])

        # Check the response status
        if response.status_code == 200:
            print(f"JSON data from {file_name} successfully sent to the URL.")
        else:
            print(f"Failed to send JSON data from {file_name}. Status code: {response.status_code}, Response: {response.text}")
            raise ValueError(f"Failed to send JSON data from {file_name}. Status code: {response.status_code}, Response: {response.text}")



def split_pdf_text(pdf_text):
    # Split the text into sections based on the delimiter
    full_text = '2025, used under license to PropTx 2025.'
    listing_strings = []
    while True:
        contact_start_index = pdf_text.find('LISTING CONTRACTED WITH')
        if contact_start_index == -1:
            print("Delimiter not found in the PDF text.")
            return listing_strings
        end_index = pdf_text.find(full_text, contact_start_index) + len(full_text)
        if pdf_text[end_index:end_index+5] == 'CO-OP':
            end_index += 6
            end_index = pdf_text.find(full_text, end_index) + len(full_text)
        listing_strings.append(pdf_text[:end_index])
        pdf_text = pdf_text[end_index:]

def create_mapping(text):
    text_mapping = []
    price = get_price(text)
    address = get_address(text)
    for name, number_type, number, role in get_phone_numbers(text):
        text_mapping.append({
        "listing": address,
        "name_or_office": name,
        "role": role,
        "number_type": number_type,
        "number": number,
        "price": price
    })
    return text_mapping


def process_pdf(pdf_text, file_name):
    split_text = split_pdf_text(pdf_text)
    print(f"Number of listings: {len(split_text)}")
    mapping_list = []
    for text in split_text:
        mapping_list += create_mapping(text)
    # mapping_list = create_mapping(split_text[4])
    print(json.dumps(mapping_list, indent=4))
    # output_csv(mapping_list, file_name)
    output_json(mapping_list, file_name)


def run_cloud_function(input_dict):
    file_name = input_dict["data"]["selfLink"].split("/")[-1]
    bucket_name = input_dict["data"]["bucket"]
    pdf_text = write_read(bucket_name, file_name)
    if pdf_text:
        process_pdf(pdf_text, file_name)
        delete_blob(bucket_name, file_name)
    else: 
        raise ValueError(f"Failed to read PDF text from {file_name}. Please check the file and try again.")

def delete_blob(bucket_name, file_name):
    """Deletes a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    blob.delete()

    print(f"Blob {file_name} deleted.")


def write_read(bucket_name, file_name):
    """Write and read a blob from GCS using file-like IO"""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The ID of your new GCS object
    # blob_name = "storage-object-name"


    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    local_file_name = datetime.datetime.now().strftime("%Y-%m-%d") + "_" + file_name
    print(f"reading {blob.name} from {bucket.name}...")
    blob.download_to_filename(local_file_name)
    print(f"Downloaded storage object {blob.name} from bucket {bucket.name} to local file {local_file_name}.")
    pdf_text = read_pdf(local_file_name)
    os.remove(local_file_name)
    return pdf_text

if __name__ == "__main__":
    # Example usage
    run_cloud_function({
        "attributes": {
            "specversion": "1.0",
            "id": "14656529786338331",
            "source": "//storage.googleapis.com/projects/_/buckets/listings-operatio",
            "type": "google.cloud.storage.object.v1.finalized",
            "datacontenttype": "application/json",
            "subject": "objects/sold6.pdf",
            "time": "2025-05-01T17:41:52.830639Z",
            "bucket": "listings-operatio"
        },
        "data": {
            "kind": "storage#object",
            "id": "listings-operatio/sold6.pdf/1746121312825704",
            "selfLink": "https://www.googleapis.com/storage/v1/b/listings-operatio/o/sold6.pdf",
            "name": "sold6.pdf",
            "bucket": "listings-operatio",
            "generation": "1746121312825704",
            "metageneration": "1",
            "contentType": "application/pdf",
            "timeCreated": "2025-05-01T17:41:52.830Z",
            "updated": "2025-05-01T17:41:52.830Z",
            "storageClass": "STANDARD",
            "timeStorageClassUpdated": "2025-05-01T17:41:52.830Z",
            "size": "2689616",
            "md5Hash": "iFI2ua2R0XAL2pQExBI2fg==",
            "mediaLink": "https://storage.googleapis.com/download/storage/v1/b/listings-operatio/o/sold6.pdf?generation=1746121312825704&alt=media",
            "crc32c": "Hj0qyQ==",
            "etag": "COji1+Togo0DEAE="
        }
    })



# fix #4