from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
import pandas as pd
import openpyxl
from random import randint
from utils import derive_date, find_el_or_null, find_els_or_null
from excel import export_to_excel, combine_old_and_new_data
from config import *

# excel_file_path = 'output.xlsx'
# max_pages = 1

def get_all_listings():
    d = driver # for easier reference
    card_element = True
    i = 0
    data = []
    while card_element != False:
        #check if job-card-x exist
        card_element = find_el_or_null(f'//*[@id="job-card-{i}"]', d)
        if card_element == False:
            break
        print(f'job-card-{i} exist')
        href_element = find_el_or_null(f'//*[@id="job-card-{i}"]//a[@data-testid="job-card-link"]', d)
        href_element = href_element.get_attribute('href').split('?')[0] if href_element != False else None

        company_element = find_el_or_null(f'//*[@id="job-card-{i}"]/*//p[@data-testid="company-hire-info"]', d)
        company_element = company_element.text if company_element != False else None
        title_element = find_el_or_null(f'//*[@id="job-card-{i}"]/*//span[@data-cy="job-card__job-title"]', d)
        title_element = title_element.text if title_element != False else None

        salary_range_bottom = find_el_or_null(f'//*[@id="job-card-{i}"]//span[@data-testid="salary-range"]/div/span[1]', d)
        salary_range_bottom = salary_range_bottom.text.replace('$', '') if salary_range_bottom != False else None
        salary_range_top = find_el_or_null(f'//*[@id="job-card-{i}"]//span[@data-testid="salary-range"]/div/span[2]', d)
        salary_range_top = salary_range_top.text.replace('to', '') if salary_range_top != False else None

        applications = find_el_or_null(f'//*[@id="job-card-{i}"]//a/div//span[@data-cy="job-card__num-of-applications"]', d)
        applications = applications.text.replace(' applications', '').replace(' application', '') if applications != False else None
        location = find_el_or_null(f'//*[@id="job-card-{i}"]//div[@class="pl3 JobCard__job-title-flex___2R-sW"]//p[@data-cy="job-card__location"]', d)
        location =  location.text if location != False else None
        date_text = find_el_or_null(f'//*[@id="job-card-{i}"]//div[contains(@class, "w-40")]//span[@data-cy="job-card-date-info"]', d) # classes containing w-40
        date_text = date_text.text if date_text != False else None # create function to determine actual date
        date_info = derive_date(date_text) if date_text != None else None

        get_data.append({
            'title': title_element,
            'company': company_element,
            'salary_range_bottom': salary_range_bottom,
            'salary_range_top': salary_range_top,
            'href': href_element,
            'applications': applications,
            'location': location,
            'date_text': date_text,
            'date_info': date_info,
            'job_description': '',
            'keywords': '',
            'relevance': '',
            'apply': ''
        })

        print(f'title_element: {title_element}')
        # print(f'salary_range_bottom: {salary_range_bottom}')
        # print(f'salary_range_top: {salary_range_top}')
        # print(f'href_element: {href_element}')
        # print(f'applications: {applications}')
        # print(f'location: {location}')
        print(f'date_text: {date_text}')
        print(f'date_info: {date_info}')
        i += 1

    # return data


# set up driver
options = Options()
options.add_experimental_option("detach", True) #to keep the driver open after the script finishes
options.add_argument('user-data-dir=C:\\Users\\USER\\Desktop\\SDE-learnings\\projects\\mycareersfuture\\profile')
options.add_argument('--profile-directory=Profile 1')

# Add additional arguments to clear the cache
options.add_argument("--disable-application-cache")
options.add_argument("--disable-cache")
options.add_argument("--disable-offline-load-stale-cache")
options.add_argument("--disk-cache-size=0")
options.add_argument("--clear-browsing-data")
options.add_argument("--delete-cookies")
options.add_argument("--clear-browsing-history")
options.add_argument("--delete-file-database")
options.add_argument("--delete-indexeddb-database")
options.add_argument("--delete-local-storage")
options.add_argument("--delete-plugin-data")

driver = webdriver.Chrome(options=options) 

# initialise get data for excel export
get_data = []

# for loop to get all pages
for i in range(0, max_pages):
    print("printing page: ", i)
    driver.get(f'https://www.mycareersfuture.gov.sg/search?search=software%20engineer&sortBy=new_posting_date&page={i}')
    time.sleep(3)
    get_all_listings()
    # get_data.append(get_all_listings())

# # Read the Excel file into a pandas DataFrame
# existing_data = pd.read_excel(excel_file_path)

try:
    # existing_data = pd.read_excel(excel_file_path) 
    # # Process the data or perform actions on the DataFrame
    # print(f"file '{excel_file_path}' found.")
    # print('Existing data...........')
    # print(existing_data)
    # print('strip extra whitespaces..........')
    # existing_data.columns = existing_data.columns.str.strip()
    # print(existing_data)
    get_data = combine_old_and_new_data(excel_file_path, get_data, 'href')

except FileNotFoundError:
    print(f"File '{excel_file_path}' not found. Creating and Exporting to {excel_file_path}.")
    
# export directly to excel
export_to_excel(get_data, excel_file_path) # note, is this line even needed if error is found?

# time.sleep(int(sec))
print(f'Completed! Export to {excel_file_path}')


# time.sleep(300)  # Let the user actually see something!
#https://stackoverflow.com/questions/56585508/invalidargumentexception-message-invalid-argument-user-data-directory-is-alre