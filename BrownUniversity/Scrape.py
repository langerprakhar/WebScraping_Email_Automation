import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

def scrape_brown_faculty_selenium(url):
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

        # Find all profile blocks
        profile_blocks = soup.find_all('li', class_='profile-list')

        for block in profile_blocks:
            # Extract faculty name using the class for name
            name_block = block.find('span', class_='profile-name')
            name = name_block.get_text(strip=True) if name_block else 'Not Available'

            # Extract faculty title using the class for title
            title_block = block.find('span', class_='profile-title')
            title = title_block.get_text(strip=True) if title_block else 'Not Available'

            # Extract research areas using the class for research area
            research_area_block = block.find('span', class_='profile-areas')
            research_area = research_area_block.get_text(strip=True) if research_area_block else 'Not Available'

            # Extract the clickable link to the detailed profile page
            link_block = block.find('a', class_='profile-link')
            link = link_block['href'] if link_block else None

            if link:
                # Click on the faculty profile link to open detailed page
                driver.get(link)

                # Wait for the page to load
                time.sleep(3)

                # Get the page source after navigating to the profile page
                profile_soup = BeautifulSoup(driver.page_source, 'html.parser')

                # Extract email from the detailed profile page
                email_block = profile_soup.find('div', class_='field field--name-field-ps-people-email')
                email = email_block.get_text(strip=True) if email_block else 'Not Available'

                # Append extracted data to the list
                faculty_data.append({
                    'Name': name,
                    'Description': title,  # Using title as description
                    'Email': email,
                    'Research Area': research_area
                })

                # Go back to the main faculty list
                driver.back()
                time.sleep(2)

        # Close the WebDriver
        driver.quit()

        # Save the data to a CSV file
        df = pd.DataFrame(faculty_data)
        df.to_csv('brown_faculty_all_data.csv', index=False)
        print("Data saved to 'brown_faculty_all_data.csv'")

    except Exception as e:
        print(f"An error occurred: {e}")

# URL of the faculty page
faculty_url = "https://cs.brown.edu/people/faculty/"
scrape_brown_faculty_selenium(faculty_url)
