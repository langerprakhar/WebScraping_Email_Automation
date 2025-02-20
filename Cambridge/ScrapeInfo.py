from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape_cambridge_faculty_selenium(url):
    # Configure the Selenium WebDriver using webdriver-manager
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--ignore-certificate-errors")
    
    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Load the main faculty page
        driver.get(url)
        time.sleep(5)  # Allow the page to load

        # Initialize list to store faculty data
        faculty_data = []

        # Locate all tbody tags (no need for the table class selector)
        tbody_tags = driver.find_elements(By.TAG_NAME, "tbody")

        for tbody in tbody_tags:
            # Find all rows (tr tags) inside this tbody
            rows = tbody.find_elements(By.TAG_NAME, "tr")

            for row in rows:
                try:
                    # Try to locate the link (a tag) inside the 'views-field-title' td
                    link_td = row.find_element(By.CSS_SELECTOR, "td.views-field.views-field-title a")
                    profile_url = link_td.get_attribute("href")

                    # Click the link to open the faculty profile
                    link_td.click()
                    time.sleep(2)  # Allow the profile page to load

                    # Extract information from the faculty profile
                    try:
                        name = driver.find_element(By.TAG_NAME, 'h1').text.strip() or "NA"
                    except:
                        name = "NA"

                    try:
                        email = driver.find_element(By.CSS_SELECTOR, 'div.field-name-field-sd-email-text div.field-item.even').text.strip() or "NA"
                    except:
                        email = "NA"

                    try:
                        research_areas_links = driver.find_elements(By.CSS_SELECTOR, 'div.group-cst-themes.field-group-div div.item-list a')
                        research_areas = ", ".join([link.text.strip() for link in research_areas_links]) or "NA"
                    except:
                        research_areas = "NA"

                    try:
                        description = driver.find_element(By.CSS_SELECTOR, 'div.group-sd-teaching div.item-list').text.strip() or "NA"
                    except:
                        description = "NA"

                    # Add the extracted data to the list
                    faculty_data.append({
                        'Name': name,
                        'Email': email,
                        'Research Areas': research_areas,
                        'Description': description
                    })

                    # Navigate back to the main page
                    driver.back()
                    time.sleep(2)  # Allow the page to reload

                except Exception as e:
                    print(f"Error processing row: {e}")
                    continue

        # Save the scraped data to a CSV file
        df = pd.DataFrame(faculty_data)
        df.to_csv('cambridge_faculty.csv', index=False)
        print("Data saved to 'cambridge_faculty.csv'")

    except Exception as e:
        print(f"An error occurred during scraping: {e}")

    finally:
        driver.quit()

# URL of the Cambridge faculty page
faculty_url = "https://www.cst.cam.ac.uk/people/directory/faculty"  # Replace with the actual URL
scrape_cambridge_faculty_selenium(faculty_url)
