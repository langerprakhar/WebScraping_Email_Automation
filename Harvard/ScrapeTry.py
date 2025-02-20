import csv
import os
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

# URLs to scrape
urls = [
    "https://seas.harvard.edu/computer-science/people",
    "https://seas.harvard.edu/computer-science/people?page=%2C1",
    "https://seas.harvard.edu/computer-science/people?page=%2C2",  # Add all your URLs here
        "https://seas.harvard.edu/computer-science/people?page=%2C3",  # Add all your URLs here
    "https://seas.harvard.edu/computer-science/people?page=%2C4",  # Add all your URLs here
    "https://seas.harvard.edu/computer-science/people?page=%2C5",  # Add all your URLs here
    "https://seas.harvard.edu/computer-science/people?page=%2C6",  # Add all your URLs here
    "https://seas.harvard.edu/computer-science/people?page=%2C7",  # Add all your URLs here
    "https://seas.harvard.edu/computer-science/people?page=%2C8",  # Add all your URLs here
    "https://seas.harvard.edu/computer-science/people?page=%2C9",  # Add all your URLs here
    "https://seas.harvard.edu/computer-science/people?page=%2C10",  # Add all your URLs here
    "https://seas.harvard.edu/computer-science/people?page=%2C11",  # Add all your URLs here
    "https://seas.harvard.edu/computer-science/people?page=%2C12",  # Add all your URLs here
    "https://seas.harvard.edu/computer-science/people?page=%2C13",  # Add all your URLs here
    "https://seas.harvard.edu/computer-science/people?page=%2C14",  # Add all your URLs here
    "https://seas.harvard.edu/computer-science/people?page=%2C15",  # Add all your URLs here
    "https://seas.harvard.edu/computer-science/people?page=%2C16",  # Add all your URLs here

    # Add further URLs...
]

# Output CSV file
output_file = "HarvardProfessors.csv"

# Check if the CSV file already exists to avoid rewriting headers
file_exists = os.path.isfile(output_file)

# Initialize CSV file (write headers if file doesn't exist)
with open(output_file, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    if not file_exists:
        writer.writerow(["Name", "Email", "Research Areas"])  # Columns (write header once)

try:
    # Loop through each URL
    for url in urls:
        driver.get(url)
        wait = WebDriverWait(driver, 30)

        # Find all professor links within the h2 elements
        professor_links = driver.find_elements(By.CSS_SELECTOR, 'h2.node-title.teaching-area-dark.person__detailed-name a')
        print(f"Found {len(professor_links)} professors on {url}")

        # Loop through all professors by index to avoid stale elements
        for index in range(len(professor_links)):
            # Refresh links each time
            professor_links = driver.find_elements(By.CSS_SELECTOR, 'h2.node-title.teaching-area-dark.person__detailed-name a')
            link = professor_links[index]
            name = link.text.strip()  # Get the professor's name
            print(f"Processing: {name}")

            try:
                # Open the professor's profile page
                ActionChains(driver).move_to_element(link).click(link).perform()
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

                # Extract email
                try:
                    email_div = driver.find_element(By.CSS_SELECTOR, 'div.person__email.person__email--full a')
                    email = email_div.text.strip()
                except Exception:
                    email = "Not Found"

                # Extract research areas
                try:
                    # Locate the parent container holding the research areas (accordion items)
                    accordion_items = driver.find_elements(By.CLASS_NAME, "accordion-item")
                    
                    # Initialize an empty list to hold all research areas
                    research_areas_list = []

                    # Loop through each accordion item
                    for item in accordion_items:
                        try:
                            # Check if this accordion item has a relevant class for research areas
                            research_area_div = item.find_element(By.CLASS_NAME, "person__research-interests")
                            
                            # Inside the research area div, locate all links (a tags) with research area text
                            links = research_area_div.find_elements(By.TAG_NAME, "a")
                            research_areas_list.extend([link.text.strip() for link in links])  # Add text to the list
                        except Exception:
                            continue  # Skip if this accordion item doesn't contain research areas

                    # Combine all research areas into a single comma-separated string
                    research_areas = ", ".join(research_areas_list) if research_areas_list else "Not Found"
                except Exception as e:
                    print(f"Error extracting research areas: {e}")
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
