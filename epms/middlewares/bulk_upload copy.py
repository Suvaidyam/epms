import csv
from datetime import datetime, timedelta
import random

def generate_random_date():
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 12, 31)
    random_days = random.randint(0, (end_date - start_date).days)
    random_date = start_date + timedelta(days=random_days)
    formatted_date = random_date.strftime("%d-%m-%Y")
    return formatted_date

def generate_random_name():
    first_names = ["Isha", "Pooja", "Nancy", "Sakshi","Khush","Samar","Abhishek", "Ananya", "Aditya", "Advait", "Avani", "Akshay", "Aisha", "Aryan"]
    last_names = ["Sharma", "Patel", "Verma", "Singh", "Joshi", "Gupta", "Kumar", "Malhotra", "Mittal", "Reddy"]
    random_first_name = random.choice(first_names)
    random_last_name = random.choice(last_names)
    random_indian_name = f"{random_first_name} {random_last_name}"
    return random_indian_name

def generate_random_number():
    start_mobile_number = 7000000000
    end_mobile_number = 9999999999
    random_mobile_number = "+91-" + str(random.randint(start_mobile_number, end_mobile_number))
    return random_mobile_number
    

genders = ["Male", "Female", "Others"]
current_occupation =["Student" , "Home Maker", "Unemployed" , "Shop Worker" , "Unemployed" , "Shop Worker" ,"Security Guard" , "Form Separately Filled" , "Factory Worker Others Helper"]
caste=["ST" , "SC" , "OBC" , "General"]
csc=["CSC-S07-064", "CSC-S07-029" ,"CSC-S07-028" ,"CSC-S07-027" ,"CSC-S07-026" ,"CSC-S07-025"]
bank_account=["No", "Yes"]
current_location =["L-CSC-S07-025-1563","L-CSC-S07-025-1564","L-CSC-S07-028-1528","L-CSC-S07-028-1529" ,"L-CSC-S07-028-1530"]
# state_of_origin=["S16", "S17" ,"S18","S19","S20","S21","S22","S23","S24","S25","S26","S27"]
state_of_origin=["S16"]
# district_of_origin=['S16292' ,'S16291' ,'S16290' ,'S16289']
district_of_origin=['S16292']
block_of_origin=["S162920040", "S162920039" ,"S162920038" ,"S162920037" ,"S162920036" ,"S162920035","S162920034" ,"S162920033"]
education=['B.Com','Post Graduate' ,'Illiterate', 'Graduate','Under Graduate','ITI/Technical','Below Primary']
source_information_about_center=["Agrasar sathi","Radio program","Self","Direct mobilization","Collectivisation"]

data_list = []
header = [
    'registration_date', 'name_of_the_beneficiary', 'contact_number', 'age', 'gender',
    'occupation', 'caste', 'csc', 'do_you_have_bank_account', 'current_location',
    'state_of_origin', 'district_of_origin', 'block_of_origin', 'education',
    'source_information_about_center', 'head_of_family', 'overall_status', 'numeric_overall_status' ,'Support category (support_table)' ,'Support name (support_table)',
    'Application submitted (support_table)',"Name of the support (followup_table)","Follow-up date (followup_table)","Follow-up status (followup_table)"
]

for i in range(20):
    new_data = {
        'registration_date': generate_random_date(),
        'name_of_the_beneficiary': generate_random_name(),
        'contact_number': generate_random_number(),
        'age': random.randint(1, 70),
        'gender': random.choice(genders),
        'occupation': random.choice(current_occupation),
        'caste': random.choice(caste),
        'csc': random.choice(csc),
        'do_you_have_bank_account': random.choice(bank_account),
        'current_location': random.choice(current_location),
        'state_of_origin': random.choice(state_of_origin),
        'district_of_origin': random.choice(district_of_origin),
        'block_of_origin': random.choice(block_of_origin),
        'education': random.choice(education),
        'source_information_about_center': random.choice(source_information_about_center),
        'head_of_family': 'No',
        'overall_status': 'Open',
        'numeric_overall_status': '0/0',
        'Support category (support_table)':"Documentation",
        'Support name (support_table)':'Family ID New',
        'Application submitted (support_table)':'No',
        'Name of the support (followup_table)':'Family ID New',
        'Follow-up date (followup_table)': generate_random_date(),
        'Follow-up status (followup_table)':'Interested'
    }
    data_list.append(new_data)

# Writing data to CSV file
csv_file_path = 'beneficiary_data.csv'
with open('./ben.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=header)
    writer.writeheader()
    writer.writerows(data_list)

print(f"CSV file generated successfully at: {csv_file_path}")