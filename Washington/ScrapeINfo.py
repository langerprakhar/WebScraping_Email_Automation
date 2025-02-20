import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up Selenium WebDriver with dynamic ChromeDriver installation
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# URL to scrape
url = "https://www.cs.washington.edu/people/faculty-members/"

# Output CSV file
output_file = "WashUFaculty.csv"

# Initialize CSV file
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Email", "Research Areas"])

# Set to store the names of processed professors
processed_professors = set()

try:
    driver.get(url)
    wait = WebDriverWait(driver, 30)

    # Loop through all professor links
    while True:
        # Refresh the list of links every time to ensure it is up-to-date
        professor_links = driver.find_elements(By.CSS_SELECTOR, "p.elementor-heading-title.elementor-size-default a")
        num_links = len(professor_links)

        if num_links == 0:
            print("No more links found.")
            break

        # Go through each link
        for i in range(num_links):
            # Re-fetch the link to avoid StaleElementReferenceException
            link = driver.find_elements(By.CSS_SELECTOR, "p.elementor-heading-title.elementor-size-default a")[i]
            name = link.text

            # Check if the professor has already been processed
            if name in processed_professors:
                print(f"Already processed: {name}. Stopping.")
                break

            print(f"Processing: {name}")  # Debugging log to track progress

            ActionChains(driver).move_to_element(link).click(link).perform()

            # Wait for the page to load
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            # Extract email
            try:
                email = driver.find_element(By.CSS_SELECTOR, "div.elementor-element-44802461 div.elementor-widget-container").text
            except Exception:
                email = "Not Found"

            # Extract all research areas (get all <a> tags in the research areas container)
            try:
                research_areas_elements = driver.find_elements(
                    By.CSS_SELECTOR,
                    "div.elementor-element-e02a911.elementor-widget-text-editor div.elementor-widget-container a"
                )
                research_areas = [ra.text for ra in research_areas_elements]  # Extract text of all <a> tags
                research_areas = ", ".join(research_areas)  # Join them into a single string
            except Exception:
                research_areas = "Not Found"

            # Save the information
            with open(output_file, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([name, email, research_areas])

            # Mark this professor as processed
            processed_professors.add(name)

            driver.back()
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(3)

        # If we broke out of the loop (because a professor is repeated), stop the script
        if name in processed_professors:
            break

finally:
    driver.quit()

print(f"Data has been saved to {output_file}.")
