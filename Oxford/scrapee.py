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

def scrape_oxford_faculty_selenium(url):
    try:
        # Setup Chrome options
        options = Options()
        options.headless = False  # Visible mode for debugging

        # Initialize WebDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # Open the URL
        driver.get(url)

        # Wait for the page to load
        time.sleep(10)

        # Find faculty links under 'personIndex'
        faculty_links = driver.find_elements(By.CSS_SELECTOR, '.personIndex a')

        # Initialize list to store faculty data
        faculty_data = []

        # List of names to skip
        skip_names = [
            "Leslie Ann Goldberg", "Alex Rogers", "Andrew Simpson", 
            "Christian Rupprecht", "Sergii Strelchuk", "Mark van der Wilk", 
            "James Worrell", "Nobuko Yoshida", "Standa Živný"
        ]

        print(f"Found {len(faculty_links)} faculty links.")
        
        for link in faculty_links:
            faculty_name = link.text.strip()

            # Skip specific faculty members
            if faculty_name in skip_names:
                print(f"Skipping {faculty_name}.")
                continue

            print(f"Clicking on faculty link: {faculty_name}")

            # Click the link to go to the detailed faculty page
            actions = ActionChains(driver)
            actions.move_to_element(link).click().perform()

            try:
                # Wait for the panel body to load
                WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'panel-body')))
            except Exception as e:
                print(f"Panel body not found for {faculty_name}. Skipping.")
                continue

            # Get the detailed page source
            soup_detail = BeautifulSoup(driver.page_source, 'html.parser')

            try:
                # Extract Name
                honorific_prefix = soup_detail.find('span', itemprop='honorificPrefix')
                given_name = soup_detail.find('span', itemprop='givenName')
                family_name = soup_detail.find('span', itemprop='familyName')
                honorific_suffix = soup_detail.find('span', itemprop='honorificSuffix')
                name = ' '.join([
                    honorific_prefix.text if honorific_prefix else '',
                    given_name.text if given_name else '',
                    family_name.text if family_name else '',
                    honorific_suffix.text if honorific_suffix else ''
                ]).strip()

                # Extract Job Title
                job_title = soup_detail.find('div', itemprop='jobTitle')
                job_title = job_title.text.strip() if job_title else 'Not Available'

                # Extract Email
                email = soup_detail.find('div', itemprop='email')
                email = email.text.strip() if email else 'Not Available'

                # Extract Research Areas from 'list-comma-separated' class
                research_area_block = soup_detail.find('ul', class_='list-comma-separated')
                research_areas = ', '.join([a.get_text(strip=True) for a in research_area_block.find_all('a')]) if research_area_block else 'Not Available'

                # Extract unordered list items in 'panel-body'
                panel_body = soup_detail.find('div', class_='panel-body')
                ul_items = panel_body.find_all('ul') if panel_body else []
                list_items = [li.get_text(strip=True) for ul in ul_items for li in ul.find_all('li')]
                research_areas_extended = ', '.join(list_items) if list_items else 'Not Available'

                # Append extracted data to the list
                faculty_data.append({
                    'Name': name,
                    'Job Title': job_title,
                    'Email': email,
                    'Research Areas': research_areas,
                    'Additional Details (UL)': research_areas_extended
                })

            except Exception as e:
                print(f"Error occurred for {faculty_name}: {e}")
                continue

            # Go back to the main page
            driver.back()

            # Wait for the main page to reload
            time.sleep(6)

        # Close the WebDriver
        driver.quit()

        # Save the data to a CSV file
        df = pd.DataFrame(faculty_data)
        df.to_csv('oxford_faculty.csv', index=False)
        print("Data saved to 'oxford_faculty.csv'")

    except Exception as e:
        print(f"An error occurred: {e}")
        if driver:
            driver.quit()

# URL of the Oxford faculty page
faculty_url = "https://www.cs.ox.ac.uk/people/faculty.html"
scrape_oxford_faculty_selenium(faculty_url)
