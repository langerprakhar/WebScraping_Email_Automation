import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Setting up the Selenium WebDriver with WebDriver Manager
def setup_driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-web-security")
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(service=service, options=options)
    return driver


# URL of the Columbia faculty page
url = "https://www.cs.columbia.edu/people/faculty/"

# Initialize the WebDriver
driver = setup_driver()

try:
    # Open the Columbia faculty page
    driver.get(url)

    # Wait for the page to load if needed
    driver.implicitly_wait(10)

    # Extract all faculty entries
    professor_elements = driver.find_elements(By.CLASS_NAME, "faculty-details")

    # Prepare data for CSV
    data = [["Name", "Email", "Research Interests"]]  # Header row

    # Extract details for each professor
    for professor in professor_elements:
        # Extract name
        try:
            name_element = professor.find_element(By.CSS_SELECTOR, "span.faculty-name a")
            name = name_element.text
        except:
            name = "N/A"

        # Extract emails
        # Extract emails
        try:
            email_elements = professor.find_elements(By.CSS_SELECTOR, "div.faculty-contact-info ul li a")
            emails = [email.text for email in email_elements if "@" in email.text]
            email = ", ".join(emails) if emails else "N/A"
        except:
            email = "N/A"


        # Extract research interests
        try:
            research_area_element = professor.find_element(By.CSS_SELECTOR, "div.faculty-interests")
            research_area = research_area_element.text
        except:
            research_area = "N/A"

        # Append to data list
        data.append([name, email, research_area])

    # Save data to a CSV file
    csv_filename = "columbia_faculty.csv"
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(data)

    print(f"Data successfully saved to {csv_filename}")

finally:
    # Close the WebDriver
    driver.quit()
