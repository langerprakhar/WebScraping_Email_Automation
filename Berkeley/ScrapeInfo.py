import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Set up Selenium WebDriver with dynamic ChromeDriver installation
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# URL to scrape
url = "https://www2.eecs.berkeley.edu/Faculty/Lists/CS/faculty.html"

# Output CSV file
output_file = "BerkeleyFaculty.csv"

# Initialize CSV file
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Email", "Research Interests"])

try:
    # Open the webpage
    print(f"Opening webpage: {url}")
    driver.get(url)

    # Find all div elements with the specified class
    faculty_divs = driver.find_elements(By.CSS_SELECTOR, "div.cc-image-list__item__content")
    print(f"Found {len(faculty_divs)} faculty entries.")

    for i, div in enumerate(faculty_divs, start=1):
        print(f"\nProcessing faculty {i}/{len(faculty_divs)}...")

        # Extract professor name from <h3><a> inside the div
        try:
            name_element = div.find_element(By.CSS_SELECTOR, "h3 a")
            name = name_element.text.strip()
            print(f"Extracted Name: {name}")
        except Exception:
            name = "Not Found"
            print("Name not found.")

        # Extract email from <p> tags
        try:
            email = None
            p_elements = div.find_elements(By.TAG_NAME, "p")
            for p in p_elements:
                text = p.text
                if "@" in text and "." in text:
                    email = text.strip()
                    break
            email = email if email else "Not Found"
            print(f"Extracted Email: {email}")
        except Exception as e:
            email = "Not Found"
            print(f"Error extracting email: {e}")

        # Extract research interests from <p><a> clickable links
        try:
            research_interests = []
            for p in p_elements:
                a_elements = p.find_elements(By.TAG_NAME, "a")
                for a in a_elements:
                    research_interests.append(a.text.strip())
            research_interests = ", ".join(research_interests) if research_interests else "Not Found"
            print(f"Extracted Research Interests: {research_interests}")
        except Exception as e:
            research_interests = "Not Found"
            print(f"Error extracting Research Interests: {e}")

        # Write the extracted data to the CSV
        with open(output_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([name, email, research_interests])

        print("Data for this faculty saved to CSV.")

finally:
    driver.quit()
    print(f"\nWeb scraping complete. Data has been saved to {output_file}.")
