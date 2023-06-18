from datetime import date, timedelta
from selenium.webdriver.common.by import By


def derive_date(text):
    text = text.lower()
    print(text)
    if (text == ''):
        print('date text is empty')
        return None
    elif (text == 'posted today'):
        return date.today()
    elif 'viewed' in text:
        return "Clear cache"
    elif (text == 'posted yesterday'):
        return date.today() - timedelta(days=1)
    else:
        print(text)
        # posted x days ago
        return date.today() - timedelta(days=int(text.split(' ')[1]))
    return None

def find_el_or_null(element, driver):
    try:
        return_element = driver.find_element(By.XPATH, element)
        print(f'exist! -> {element}')
        return return_element
    except:
        print(f'{element} does not exist')
        return False


def find_els_or_null(element, driver):
    try:
        return_element = driver.find_elements(By.XPATH, element)
        print(f'exist! -> {element}')
        return return_element
    except:
        print(f'{element} does not exist')
        return False