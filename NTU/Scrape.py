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
url = "https://www.ntu.edu.sg/computing/our-people/faculty"

# Output CSV file
output_file = "NTUFaculty.csv"

# Initialize CSV file
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Email", "Research Areas"])  # Columns

try:
    # Open the target URL
    driver.get(url)
    wait = WebDriverWait(driver, 30)

    # Click on the div to open the list of professors
    faculty_div = wait.until(EC.element_to_be_clickable((By.ID, "Content_C008_Col00")))
    faculty_div.click()

    # Wait for the list of professors to load
    time.sleep(2)  # Add a brief delay for dynamic content to load

    # Find all professor links within the h3 elements
    professor_links = driver.find_elements(By.CSS_SELECTOR, 'h3.img-card__title a')

    for link in professor_links:
        name = link.text.strip()  # Get the professor's name
        print(f"Processing: {name}")

        try:
            # Open the professor's profile page
            ActionChains(driver).move_to_element(link).click(link).perform()
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            # Extract email
            try:
                email_div = driver.find_element(By.CLASS_NAME, "dynaFieldValue")
                email = email_div.text.strip()
            except Exception:
                email = "Not Found"

            # Extract research areas
            try:
                # Click on the "Research Areas" panel to reveal the content
                research_panel = driver.find_element(By.CLASS_NAME, "panel-heading")
                ActionChains(driver).move_to_element(research_panel).click(research_panel).perform()
                time.sleep(1)  # Wait for content to expand

                # Extract research areas content
                research_div = driver.find_element(By.ID, "researchinterestsDiv")
                research_areas = research_div.text.strip()
            except Exception:
                research_areas = "Not Found"

            # Save to CSV
            with open(output_file, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([name, email, research_areas])

        except Exception as e:
            print(f"Error processing {name}: {e}")

        finally:
            # Navigate back to the main page
            driver.back()
            wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(2)  # Allow the page to reload

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()

print(f"Data has been saved to {output_file}.")
