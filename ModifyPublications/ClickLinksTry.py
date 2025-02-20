import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def google_sign_in(driver, email, password):
    """Automate Google Sign-In."""
    driver.get("https://scholar.google.com/")
    
    # Click the sign-in link
    sign_in_button = driver.find_element(By.ID, "gs_hdr_act_s")
    sign_in_button.click()
    
    # Wait for the login page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "identifierId"))
    )
    
    # Enter the email
    email_input = driver.find_element(By.ID, "identifierId")
    email_input.send_keys(email)
    driver.find_element(By.ID, "identifierNext").click()
    
    # Wait for password field to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    
    # Enter the password
    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys(password)
    driver.find_element(By.ID, "passwordNext").click()
    
    # Wait for the login process to complete (wait for the Scholar homepage)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "gs_hdr_mnu"))
    )
    print("Successfully signed in to Google Scholar.")

def extract_pdf_links(url, driver):
    """Extract PDF links from a given URL."""
    driver.get(url)
    
    # Wait for page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "gs_or_ggsm"))
    )
    
    pdf_links = []
    # Find all divs with class 'gs_or_ggsm'
    pdf_divs = driver.find_elements(By.CLASS_NAME, "gs_or_ggsm")
    
    for div in pdf_divs:
        try:
            # Find the <a> tag inside the div and get the href attribute
            pdf_link = div.find_element(By.TAG_NAME, "a").get_attribute("href")
            if pdf_link:
                pdf_links.append(pdf_link)
        except Exception as e:
            print(f"Error extracting PDF link: {e}")
    
    return pdf_links

def process_csv(input_csv, output_csv, email, password):
    """Sign in and process each URL from the CSV to extract PDF links."""
    # Setup the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    # Perform Google Sign-In
    google_sign_in(driver, email, password)
    
    # Read the input CSV
    df = pd.read_csv(input_csv)
    
    extracted_data = []
    for _, row in df.iterrows():
        url = row.get("url")
        if url:
            print(f"Processing URL: {url}")
            try:
                pdf_links = extract_pdf_links(url, driver)
                extracted_data.append({"Original_URL": url, "PDF_Links": ", ".join(pdf_links)})
            except Exception as e:
                print(f"Error processing URL {url}: {e}")
    
    # Save extracted data to a new CSV
    extracted_df = pd.DataFrame(extracted_data)
    extracted_df.to_csv(output_csv, index=False)
    print(f"Saved extracted PDF links to {output_csv}")
    
    driver.quit()

# Example usage
if __name__ == "__main__":
    input_csv = "Top_Cited_Publications_With_URLs.csv"  # Replace with your input CSV
    output_csv = "Extracted_PDF_Links.csv"  # Replace with desired output file
    email = "codingguru3999@gmail.com"  # Replace with your email
    password = "Jeeaspirant@123"  # Replace with your password
    
    process_csv(input_csv, output_csv, email, password)
