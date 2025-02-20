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

def scrape_stanford_faculty_selenium(url):
    try:
        # Setup Chrome options
        options = Options()
        options.headless = False  # Visible mode for debugging

        # Initialize WebDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # Open the URL
        driver.get(url)

        # Wait for the page to load
        time.sleep(3)

        # Initialize list to store faculty data
        faculty_data = []

        # Loop to find faculty links and click "Load More" if necessary
        while True:
            # Find all faculty links in the content div
            faculty_links = driver.find_elements(By.CSS_SELECTOR, '.node.stanford-person a')

            # If no more faculty links found, break the loop
            if len(faculty_links) == 0:
                print("No more faculty links found. Exiting.")
                break

            print(f"Found {len(faculty_links)} faculty links.")

            # Iterate over the faculty links
            for link in faculty_links:
                faculty_name = link.text.strip()

                print(f"Clicking on faculty link: {faculty_name}")

                # Click the link to go to the detailed faculty page
                actions = ActionChains(driver)
                actions.move_to_element(link).click().perform()

                # Wait for the page to load
                time.sleep(3)

                # Get the detailed page source
                soup_detail = BeautifulSoup(driver.page_source, 'html.parser')

                try:
                    # Extract Name
                    name_elem = soup_detail.find('div', class_='node stanford-person node-title ds label-hidden')
                    name = name_elem.text.strip() if name_elem else 'Not Available'

                    # Extract Description (Short Title)
                    description_elem = soup_detail.find('div', class_='node stanford-person su-person-short-title string label-hidden')
                    description = description_elem.text.strip() if description_elem else 'Not Available'

                    # Extract Email
                    email_elem = soup_detail.find('div', class_='su-person-email node stanford-person email label-hidden')
                    email = email_elem.text.strip() if email_elem else 'Not Available'

                    # Extract Research Areas (looking for h2 tags)
                    research_areas = []
                    for h2_tag in soup_detail.find_all('h2'):
                        research_area = h2_tag.text.strip()
                        if research_area:  # Avoid empty entries
                            research_areas.append(research_area)

                    # Create one entry per research area if it matches AI/ML
                    for research_area in research_areas:
                        if 'AI' in research_area or 'ML' in research_area:
                            faculty_data.append({
                                'Name': name,
                                'Description': description,
                                'Email': email,
                                'Research Area': research_area
                            })

                except Exception as e:
                    print(f"Error occurred for {faculty_name}: {e}")
                    continue

                # Go back to the main page
                driver.back()

                # Wait for the main page to reload
                time.sleep(10)

                # Re-locate faculty links after navigating back
                faculty_links = driver.find_elements(By.CSS_SELECTOR, '.node.stanford-person a')

            # Click on "Load More" button if it exists
            try:
                load_more_button = driver.find_element(By.CSS_SELECTOR, '.pager__item')
                load_more_button.click()
                time.sleep(10)  # Wait for more faculty links to load
            except:
                print("No more 'Load More' button found. Exiting.")
                break

        # Close the WebDriver
        driver.quit()

        # Save the data to a CSV file
        df = pd.DataFrame(faculty_data)
        df.to_csv('stanford_faculty.csv', index=False)
        print("Data saved to 'stanford_faculty.csv'")

    except Exception as e:
        print(f"An error occurred: {e}")
        if driver:
            driver.quit()

# URL of the Stanford faculty page
faculty_url = "https://www.cs.stanford.edu/people/faculty-research-focus"
scrape_stanford_faculty_selenium(faculty_url)
