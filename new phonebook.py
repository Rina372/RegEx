from pprint import pprint
import re
import csv
from collections import defaultdict


with open("phonebook_raw.csv") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

    phone_number = r'(\+7|8|7)?[\s*|-]?\(?(\d{3})\)?[\s*|-]?(\d{3})[\s*|-]?(\d{2})[\s*|-]?(\d{2})[\s*|-]?\(?((доб)\.?)\s*(\d+)\)?'
    correct_phone = r'+7(\2)\3-\4-\5\6\7'

    list_correct = []
    for page in contacts_list:
        page_string = ','.join(page)
        page_format = re.sub(phone_number, phone_number, page_string)
        page_list = page_format.split(',')
        list_correct.append(page_list)


    pattern_name = r'(^\w[А-ё]+)[\s+|,]?(\w[А-ё]+)[\s+|,]?(\w[А-ё]+)?'
    new_name = r'\1 \2 \3'

    contacts_list = []
    for page in list_correct:
        page_string = ','.join(page)
        page_format = re.sub(pattern_name, new_name, page_string)
        page_list = page_format.split(',')
        if page_list not in contacts_list:
            contacts_list.append(page_list)

no_duplicates = defaultdict(list)
for data in list_correct:
    key = tuple(data[:2])
    for item in data:
        if item not in no_duplicates[key]:
            no_duplicates[key].append(item)

correct_result = list(no_duplicates.values())
pprint(correct_result)

for contact in correct_result:
    if len(contact) == 7:
        if '@' not in contact[6] and 'email' not in contact[6]:
            contact.insert(4, contact[6])
            del contact[5]
            contact[6] = ''
            print(contact)

with open("phonebook.csv", "w") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(correct_result)

