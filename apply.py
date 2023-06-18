from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
import time
from selenium.webdriver.common.by import By
import pandas as pd
import openpyxl
from random import randint
from utils import derive_date, find_el_or_null
from excel import extract_column_rows, export_to_existing_excel, find_first_blank_row, export_to_excel
from tokenization import extract_keywords

excel_file_path = 'output.xlsx'

def apply_to_job(driver, url):
    driver.get(url) # go to url
    try:
        # if application already been submitted, redirected to error page
        # note: elements, not element, no error thrown if not found unlike find_element. it reutrns empty list
        error_page = driver.find_elements(By.XPATH, '//*[@id="job-not-permitted-page"]')
        if len(error_page) > 0:
            return 'applied' # already applied

        # Wait for login and visibility of the "Next" button
        WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="application-details-save-button"]')))

        # Once we're logged in and the "Next" button is visible, proceed with clicking it
        next_button = driver.find_element(By.XPATH,'//*[@id="application-details-save-button"]')
        next_button.click()

        # Wait for login and visibility of the "Submit" button
        WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="react-root"]//button[@data-cy="job-application-review__submit-button"]')))

        # Click the "Submit" button
        submit_button = driver.find_element(By.XPATH,'//*[@id="react-root"]//button[@data-cy="job-application-review__submit-button"]')
        submit_button.click()

        # Wait until the success message is visible
        WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="react-root"]//div[@data-testid="submission-success-text"]')))
        return 'applied' # success

    except NoSuchElementException:
        print(f'Could not complete application at {url}.')
        return 'Element not found'
    except Exception as e:
        print(f'An error occurred: {str(e)}')
        return 'Error'


# set up driver
options = Options()
options.add_experimental_option("detach", True) #to keep the driver open after the script finishes
options.add_argument('user-data-dir=C:\\Users\\USER\\Desktop\\SDE-learnings\\projects\\mycareersfuture\\profile')
options.add_argument('--profile-directory=Profile 1')

driver = webdriver.Chrome(options=options)
# print(f'driver.command_executor._url: {driver.command_executor._url}')
# print(f'driver.session_id: {driver.session_id}')

# Read the Excel file into a pandas DataFrame
data_frame = pd.read_excel(excel_file_path)


# on first session, you will encounter login page
# continue only when you have logged in and //*[@id="application-details-save-button"] is visible


## Loop over each row in the DataFrame. For each row, it provides the index of the row and the row itself.
for index, row in data_frame.iterrows():

    # Check if the value in the 'apply_column_name' column of the current row is 1
    if row['apply'] == 1:

        href_url = row['href'] # get the url from the 'href' column of the current row
        apply_url = href_url + '/apply' # This will be the url we navigate to in order to apply.

        # Call the function apply_to_job, which is responsible for applying to the job
        # We pass the Selenium browser instance and the apply url to this function.
        isSuccess = apply_to_job(driver, apply_url)

        if isSuccess == 'applied':
            # After applying to the job, update the 'apply_column_name' of the current row in the DataFrame.
            # We change the value from 1 to 'applied' to indicate that we have applied to this job.
            data_frame.at[index, 'apply'] = 'applied'

# Save the updated DataFrame back to the Excel file
data_frame.to_excel(excel_file_path, index=False)

# # Close the browser once done
# browser.quit()


print('Completed!')

# time.sleep(300)  # Let the user actually see something!
#https://stackoverflow.com/questions/56585508/invalidargumentexception-message-invalid-argument-user-data-directory-is-alre