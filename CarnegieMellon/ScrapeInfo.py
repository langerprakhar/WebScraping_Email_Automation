from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
import time

# Set up Selenium WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# URL to scrape
url = "https://csd.cmu.edu/people/all"

# Output CSV file
output_file = "CMUFaculty.csv"

# Initialize CSV file
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Email", "Research Interests"])  # Columns

# Set to store the names of processed professors
processed_professors = set()

try:
    driver.get(url)
    wait = WebDriverWait(driver, 30)

    while True:  # Loop through all pages
        # Wait for the table to load
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'td[headers="view-field-first-name-table-column"] a')))

        # Locate professor links inside the table
        professor_rows = driver.find_elements(By.CSS_SELECTOR, 'td[headers="view-field-first-name-table-column"] a')

        for index in range(len(professor_rows)):
            # Re-fetch the rows dynamically to avoid stale references
            professor_rows = driver.find_elements(By.CSS_SELECTOR, 'td[headers="view-field-first-name-table-column"] a')
            if index >= len(professor_rows):
                break

            link = professor_rows[index]
            name = link.text.strip()

            # Skip if already processed
            if name in processed_professors:
                print(f"Already processed: {name}. Skipping.")
                continue

            print(f"Processing: {name}")

            # Click the professor's link to open their profile
            try:
                ActionChains(driver).move_to_element(link).click(link).perform()

                # Wait for the profile page to load
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

                # Extract email
                try:
                    email_container = driver.find_element(By.CSS_SELECTOR, "div.info-cell1")
                    email_text = email_container.text.strip()
                    email = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", email_text)
                    email = email.group() if email else "Not Found"
                except Exception:
                    email = "Not Found"

                # Extract research interests
                try:
                    research_interests_container = driver.find_elements(By.CSS_SELECTOR, "div.info-cell2 p")
                    research_interests_text = ""
                    for p in research_interests_container:
                        if "Research Interests" in p.text:
                            research_interests_text = p.text.replace("Research Interests", "").strip()
                            break
                    research_interests = research_interests_text if research_interests_text else "Not Found"
                except Exception:
                    research_interests = "Not Found"

                # Save to CSV
                with open(output_file, mode='a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([name, email, research_interests])

                # Mark as processed
                processed_professors.add(name)

            except Exception as e:
                print(f"Error processing {name}: {e}")

            finally:
                # Return to the main faculty page
                driver.back()
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'td[headers="view-field-first-name-table-column"] a')))
                time.sleep(2)  # Allow the page to load

        # Check for "Next" page button
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'ul.pager__items li.pager__item a[rel="next"]')
            if next_button.is_displayed() and next_button.is_enabled():
                print("Navigating to next page...")
                ActionChains(driver).move_to_element(next_button).click(next_button).perform()
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'td[headers="view-field-first-name-table-column"] a')))
                time.sleep(3)  # Allow the page to load
            else:
                print("No more pages. Exiting pagination loop.")
                break
        except Exception:
            print("No more pages. Exiting pagination loop.")
            break

finally:
    driver.quit()

print(f"Data has been saved to {output_file}.")
