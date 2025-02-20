import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

def scrape_princeton_faculty_selenium(url):
    try:
        # Setup Chrome options to run Selenium
        options = Options()
        options.headless = True  # Run in headless mode (without opening browser window)

        # Initialize the WebDriver (this will automatically manage the driver version)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # Open the URL
        driver.get(url)

        # Wait for the page to load (for 5 seconds here)
        time.sleep(5)

        # Get the page source after the page is rendered
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Initialize list to store faculty data
        faculty_data = []

        # Find all faculty entries in the relevant blocks
        faculty_blocks = soup.find_all('div', class_='content-list-item-details')

        for block in faculty_blocks:
            # Extract name using the class for the title
            name_block = block.find('span', class_='field field--name-title field--type-string field--label-hidden')
            name = name_block.get_text(strip=True) if name_block else 'Not Available'

            # Extract description using the class for position
            description_block = block.find('div', class_='field field--name-field-ps-people-position field--type-string field--label-hidden field__item')
            description = description_block.get_text(strip=True) if description_block else 'Not Available'

            # Extract email using the correct inner class for the email
            email_block = block.find('div', class_='field field--name-field-ps-people-email field--type-email field--label-inline clearfix')
            email_inner_block = email_block.find('div', class_='field__item') if email_block else None
            email = email_inner_block.get_text(strip=True) if email_inner_block else 'Not Available'

            # Extract research area using the relevant class
            research_area_block = block.find('div', class_='field--type-entity-reference-taxonomy-term field field--name-field-molbio-research-area field--type-entity-reference field--label-hidden field__items')
            research_area = research_area_block.get_text(strip=True) if research_area_block else 'Not Available'

            # Append extracted data to the list
            faculty_data.append({
                'Name': name,
                'Description': description,
                'Email': email,
                'Research Area': research_area
            })

        # Close the WebDriver
        driver.quit()

        # Save the data to a CSV file
        df = pd.DataFrame(faculty_data)
        df.to_csv('princeton_faculty_all_data.csv', index=False)
        print("Data saved to 'princeton_faculty_all_data.csv'")

    except Exception as e:
        print(f"An error occurred: {e}")

# URL of the faculty page
faculty_url = "https://molbio.princeton.edu/faculty"
scrape_princeton_faculty_selenium(faculty_url)
