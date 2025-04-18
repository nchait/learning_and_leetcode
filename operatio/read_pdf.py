import PyPDF2
import re
import json
import csv
import os
import logging

def get_address(data):
    first_line = data.split('\n')[0]
    return first_line

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
        name = name_and_role
        role = "LISTED"
    if is_coop:
        role += " (CO-OP)"
    if len(sections) == 1:
        return [(name, "", "", role)]
    numbers = sections[1:]
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
    numbers_str = data.split('LISTING CONTRACTED WITH')[1]
    numbers_str = numbers_str.split('(')[0]
    numbers_str = numbers_str.replace('\n \n', '\n').replace('\nPHONE\n', ' | PHONE: ').replace('\nFAX\n', ' | FAX: ')
    other_numbers = re.findall(r"\n\d{3}-\d{3}-\d{4}", numbers_str)
    for other_number in other_numbers:
        numbers_str = numbers_str.replace(other_number, " | LISTED: " + other_number[1:])
    number_str_lines = numbers_str.split('\n')
    cleaned_lines = [line for line in number_str_lines
        if not (re.match(r"^\s$", line) 
            or line.startswith('Prepared By:')
            or line.startswith('KONFIDIS')
            or line.startswith('Printed on')
            or line.startswith('PropTx Innovations')
            or line.startswith('WATERFRONT')
            or line == '')]
    return '\n'.join(cleaned_lines)

def get_phone_numbers(data):
    cleaned_data = cleanup_numbers(data)
    print(cleaned_data)
    output = []
    if 'CO-OP' in cleaned_data:
        non_coop_section, coop_section = cleaned_data.split('CO-OP\n')
        for non_coop_line in non_coop_section.split('\n'):
            output += get_numbers(non_coop_line, False)
        for coop_line in coop_section.split('\n'):
            output += get_numbers(non_coop_line, True)
    #     for non_coop_line in non_coop_section.split('\n'):
    #         if not re.match(r"^\d{3}-\d{3}-\d{4}$", non_coop_line):
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

if __name__ == "__main__":
    pdf_folder_path = "/Users/noahchait/Documents/python tests/learning_and_leetcode/operatio/pdfs"  # Folder containing PDFs

    mapping = []

    # Iterate through all PDF files in the folder
    for file_name in os.listdir(pdf_folder_path):
        if file_name.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder_path, file_name)
            pdf_text = read_pdf(pdf_path)
            # print(pdf_text)
            if pdf_text:
                split_text = split_pdf_text(pdf_text)
                print(f"Number of listings: {len(split_text)}")
                mapping_list = []
                for text in split_text:
                    mapping_list += create_mapping(text)
                # mapping_list = create_mapping(split_text[5])
                print(json.dumps(mapping_list, indent=4))
                output_csv(mapping_list, file_name)

