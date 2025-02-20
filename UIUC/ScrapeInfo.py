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
url = "https://siebelschool.illinois.edu/about/people/all-faculty"

# Output CSV file
output_file = "IllinoisFaculty.csv"

# Initialize CSV file
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Email", "Research Areas"])

# Set to store the names of processed professors
processed_professors = set()

try:
    driver.get(url)
    wait = WebDriverWait(driver, 30)

    # Scroll to load all faculty details
    while True:
        faculty_divs = driver.find_elements(By.CSS_SELECTOR, "div.details")
        last_position = driver.execute_script("return window.pageYOffset;")
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(1)  # Wait for lazy-loaded content
        new_position = driver.execute_script("return window.pageYOffset;")
        if new_position == last_position:
            break  # Stop scrolling if the page doesn't move further

    print("All faculty members loaded.")

    # Process all faculty members
    faculty_divs = driver.find_elements(By.CSS_SELECTOR, "div.details")
    for faculty in faculty_divs:
        # Extract the name and clickable link
        try:
            name_element = faculty.find_element(By.CSS_SELECTOR, "div.name a")
            name = name_element.text.strip()
            link = name_element.get_attribute("href")
        except Exception:
            continue

        # Check if the professor has already been processed
        if name in processed_professors:
            print(f"Already processed: {name}. Skipping.")
            continue

        print(f"Processing: {name}")

        # Navigate to the professor's page
        driver.get(link)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Extract email
        try:
            email_element = driver.find_element(By.CSS_SELECTOR, "div.email a")
            email = email_element.text.strip()
        except Exception:
            email = "Not Found"

        # Extract research areas
        try:
            research_areas_ul = driver.find_element(By.CSS_SELECTOR, "div.extProfileAREA ul")
            research_areas = [
                item.text.strip()
                for item in research_areas_ul.find_elements(By.TAG_NAME, "a")
                if item.text.strip()
            ]
            research_areas = ", ".join(research_areas)
        except Exception:
            research_areas = "Not Found"

        # Save the information
        with open(output_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([name, email, research_areas])

        # Mark this professor as processed
        processed_professors.add(name)

        # Go back to the main page
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

finally:
    driver.quit()

print(f"Data has been saved to {output_file}.")
