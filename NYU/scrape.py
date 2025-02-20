import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Setting up the Selenium WebDriver with WebDriver Manager
def setup_driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode if desired
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# URL of the NYU faculty page
url = "https://cs.nyu.edu/dynamic/people/faculty/"

# Initialize the WebDriver
driver = setup_driver()

try:
    # Open the NYU faculty page
    driver.get(url)

    # Wait for the page to load if needed
    driver.implicitly_wait(10)

    # Extract all professor elements
    professor_elements = driver.find_elements(By.CLASS_NAME, "col-sm-6")

    # Prepare data for CSV
    data = [["Name", "Details"]]  # Header row

    # Extract details for each professor
    for professor in professor_elements:
        # Extract name
        name_element = professor.find_element(By.CSS_SELECTOR, "div.col-sm-8.col-xs-6 p.name.bold a")
        name = name_element.text

        # Extract all "info" elements
        info_elements = professor.find_elements(By.CSS_SELECTOR, "div.col-sm-8.col-xs-6 p.info")
        details = "\n".join([info.text for info in info_elements])

        # Append to data list
        data.append([name, details])

    # Save data to a CSV file
    csv_filename = "nyu_faculty.csv"
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(data)

    print(f"Data successfully saved to {csv_filename}")

finally:
    # Close the WebDriver
    driver.quit()
