import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import re
def scrape_oxford_faculty_selenium_first_three(url):
    try:
        # Setup Chrome options to run Selenium
        options = Options()
        options.headless = False  # Run in visible mode for debugging

        # Initialize the WebDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # Open the URL
        driver.get(url)

        # Wait for the page to load
        time.sleep(10)

        # Find the list of faculty links under the class 'personIndex'
        faculty_links = driver.find_elements(By.CSS_SELECTOR, '.personIndex a')

        # Limit to the first three links
        faculty_links = faculty_links[:3]

        # Initialize list to store faculty data
        faculty_data = []

        print(f"Processing the first {len(faculty_links)} faculty links.")

        for link in faculty_links:
            faculty_name = link.text.strip()
            print(f"Clicking on faculty link: {faculty_name}")

            # Click the link to go to the detailed faculty page
            actions = ActionChains(driver)
            actions.move_to_element(link).click().perform()

            try:
                # Wait for the panel body to load
                WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'panel-body')))
            except Exception as e:
                print(f"Panel body not found for faculty {faculty_name}. Skipping to the next one.")
                continue  # Skip this iteration and move to the next link

            # Get the detailed page source
            soup_detail = BeautifulSoup(driver.page_source, 'html.parser')

            try:
                # Extract Job Title
                job_title = soup_detail.find('div', itemprop='jobTitle')
                job_title = job_title.text.strip() if job_title else 'Not Available'

                # Extract Email
                email = soup_detail.find('div', itemprop='email')
                email = email.text.strip() if email else 'Not Available'

                # Append extracted data to the list
                faculty_data.append({
                    'Faculty Name': faculty_name,
                    'Job Title': job_title,
                    'Email': email
                })

                print(f"Extracted data for {faculty_name}: Job Title: {job_title}, Email: {email}")

            except Exception as e:
                print(f"Error occurred for faculty {faculty_name}: {e}")
                continue  # Skip this iteration and move to the next faculty link

            # Go back to the main page
            driver.back()

            # Wait for the main page to load again
            time.sleep(6)

        # Close the WebDriver
        driver.quit()

        # Save the data to a CSV file
        df = pd.DataFrame(faculty_data)
        df.to_csv('oxford_faculty_first_three.csv', index=False)
        print("Data saved to 'oxford_faculty_first_three.csv'")

    except Exception as e:
        print(f"An error occurred: {e}")
        if driver:
            driver.quit()

# URL of the Oxford faculty page
faculty_url = "https://www.cs.ox.ac.uk/people/faculty.html"
scrape_oxford_faculty_selenium_first_three(faculty_url)
