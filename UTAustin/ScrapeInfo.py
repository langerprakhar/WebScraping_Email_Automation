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
url = "https://www.cs.utexas.edu/people"

# Output CSV file
output_file = "UTAustinFaculty.csv"

# Initialize CSV file
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Email", "Research Areas", "Description"])

# Set to store the names of processed professors
processed_professors = set()

try:
    driver.get(url)
    wait = WebDriverWait(driver, 30)

    # Loop through all professor links
    while True:
        # Refresh the list of professor links dynamically
        professor_links = driver.find_elements(By.CSS_SELECTOR, "div.views-field.views-field-title span.field-content a")
        num_links = len(professor_links)

        if num_links == 0:
            print("No more links found.")
            break

        for i in range(num_links):
            # Re-fetch the list of elements to avoid stale references
            professor_links = driver.find_elements(By.CSS_SELECTOR, "div.views-field.views-field-title span.field-content a")
            
            # Check if the index is valid
            if i >= len(professor_links):
                break

            link = professor_links[i]
            name = link.text

            # Check if the professor has already been processed
            if name in processed_professors:
                print(f"Already processed: {name}. Skipping.")
                continue

            print(f"Processing: {name}")  # Debugging log to track progress

            ActionChains(driver).move_to_element(link).click(link).perform()

            # Wait for the page to load
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            # Extract email
            try:
                email_element = driver.find_element(By.CSS_SELECTOR, "div.faculty-contact div.contact-field.contact-email")
                email = email_element.text.strip()
            except Exception:
                email = "Not Found"

            # Extract description
            try:
                description_element = driver.find_element(By.CSS_SELECTOR, "div.faculty-contact div.contact-title")
                description = description_element.text.strip()
            except Exception:
                description = "Not Found"

            # Extract research areas
            try:
                # First attempt to find research areas in <ul> inside toggled-section
                research_areas_elements = driver.find_elements(By.CSS_SELECTOR, "div.toggled-section ul.research-areas li a")
                research_areas = [ra.text.strip() for ra in research_areas_elements if ra.text.strip()]

                # If not found, attempt to extract from <div class="faculty-interest-subhead">
                if not research_areas:
                    research_areas_div = driver.find_element(By.CSS_SELECTOR, "div.faculty-interest-subhead")

                    # Check for the presence of "Research Interests" string
                    if "Research Interests" in research_areas_div.text:
                        # Extract <p> tags
                        p_elements = research_areas_div.find_elements(By.TAG_NAME, "p")
                        for p in p_elements:
                            research_areas.append(p.text.strip())

                research_areas = ", ".join(research_areas)
            except Exception:
                research_areas = "Not Found"

            # Check if critical information is missing; skip if so
            if email == "Not Found" and research_areas == "Not Found":
                print(f"Skipping {name} due to missing critical information.")
                driver.back()
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                continue

            # Save the information
            with open(output_file, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([name, email, research_areas, description])

            # Mark this professor as processed
            processed_professors.add(name)

            driver.back()
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(3)

        # Break out of the loop if all professors have been processed
        if len(processed_professors) == num_links:
            break

finally:
    driver.quit()

print(f"Data has been saved to {output_file}.")
