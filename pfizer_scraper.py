from selenium import webdriver
from selenium.webdriver.common.by import By
from app.utils import scrape_to_database
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from app import app, db
driver = webdriver.Chrome()
driver.get('https://data.cdc.gov/Vaccinations/COVID-19-Vaccine-Distribution-Allocations-by-Juris/saz5-9hgg/data')

while True:
    try:
        next_button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CLASS_NAME, 'pager-button-next')))
        entries = driver.find_elements(By.XPATH, '//tr/td/div')
        scrape_to_database(entries, 'Pfizer')
        next_button.click()
    except TimeoutException:
        # Handle the StaleElementReferenceException
        final_entries = driver.find_elements(By.XPATH, '//tr/td/div')
        scrape_to_database(final_entries, 'Pfizer')
        break  # Exit the loop when the last page is reached
    except StaleElementReferenceException:
        continue

# Quit the driver
driver.quit()