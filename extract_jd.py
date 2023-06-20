from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
import pandas as pd
import openpyxl
from random import randint
from utils import derive_date, find_el_or_null, find_els_or_null, derive_date_jd
from excel import extract_column_rows, export_to_existing_excel, find_first_blank_row, export_to_excel
from tokenization import extract_keywords

excel_file_path = 'output.xlsx'

def extract_job_description():
    d = driver # for easier reference
    date_info = find_el_or_null('//*[@id="last_posted_date"]', d)
    date_info = derive_date_jd(date_info.text) if date_info != False else None

    print(date_info)
    job_description = find_els_or_null(f'//div[@id="job_description"]//*[self::p or self::li or self::strong]', d)
    combined_text = ' '.join(p_tag.text for p_tag in job_description)
    print(combined_text)
    # job_description = job_description.text if job_description != False else None
    

    get_data.append({
        'date_info': date_info,
        'job_description': combined_text,
        'keywords': [],
        'relevance': 0
    })

    return combined_text

# set up driver
options = Options()
options.add_experimental_option("detach", True) #to keep the driver open after the script finishes
options.add_argument('user-data-dir=C:\\Users\\USER\\Desktop\\SDE-learnings\\projects\\mycareersfuture\\profile')
options.add_argument('--profile-directory=Profile 1')
driver = webdriver.Chrome(options=options) 
# print(f'driver.command_executor._url: {driver.command_executor._url}')
# print(f'driver.session_id: {driver.session_id}')

# initialise get data for excel export
get_data = []
start_row = find_first_blank_row(excel_file_path, 'job_description')
print(start_row, 'start row')
# get href list
href_list = extract_column_rows(excel_file_path, 'href', start_row)

# for loop to get all job listings pages
for index, url in enumerate(href_list):
    # if index > 0:
    #     print("breaking, index bigger than 1")
    #     break
    print(f"printing page index: {index}, from url: {url}")
    driver.get(url)
    time.sleep(3)
    job_description = extract_job_description()
    keywords = extract_keywords(job_description)
    get_data[index]['keywords'] = str(keywords) # convert to string for correct formatting in excel
    get_data[index]['relevance'] = len(keywords)

print(f'get data {get_data}')
export_to_existing_excel(excel_file_path, get_data, start_row)

print('Completed!')

# time.sleep(300)  # Let the user actually see something!
#https://stackoverflow.com/questions/56585508/invalidargumentexception-message-invalid-argument-user-data-directory-is-alre