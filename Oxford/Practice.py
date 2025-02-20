import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

def extract_list_comma_separated(url):
    try:
        # Setup Chrome options
        options = Options()
        options.headless = False  # Set to True to run in headless mode
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # Open the URL
        driver.get(url)

        # Wait for the element with class 'list-comma-separated' to load
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "list-comma-separated")))

        # Get the page source
        page_source = driver.page_source

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find the ul or other element with the class 'list-comma-separated'
        list_comma_separated = soup.find('ul', class_='list-comma-separated')

        if list_comma_separated:
            print("Found 'ul' with class 'list-comma-separated'. Extracting text...")
            # Extract and print the text content of the clickable links inside
            comma_separated_links = [link.get_text(strip=True) for link in list_comma_separated.find_all('a')]
            print(f"Extracted Text: {', '.join(comma_separated_links)}")
        else:
            print("No 'div' with class 'list-comma-separated' found.")

        # Close the WebDriver
        driver.quit()

    except Exception as e:
        print(f"An error occurred: {e}")

# URL to test
url = "https://www.cs.ox.ac.uk/people/alessandro.abate/"
extract_list_comma_separated(url)
