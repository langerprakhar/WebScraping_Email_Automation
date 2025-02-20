import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from transformers import BartForConditionalGeneration, BartTokenizer

# Initialize BART model and tokenizer
model_name = "facebook/bart-large-cnn"
bart_model = BartForConditionalGeneration.from_pretrained(model_name)
bart_tokenizer = BartTokenizer.from_pretrained(model_name)

# Function to summarize text using BART
def summarize_with_bart(text):
    try:
        inputs = bart_tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
        summary_ids = bart_model.generate(inputs, max_length=200, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
        return bart_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    except Exception as e:
        print(f"Error in summarizing with BART: {e}")
        return "Summary could not be generated."

# Function to get all clickable links from a URL
def get_clickable_links(url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "gs_rt")))

        elements = driver.find_elements(By.CLASS_NAME, "gs_rt")
        links = [elem.find_element(By.TAG_NAME, "a").get_attribute("href") for elem in elements if elem.find_element(By.TAG_NAME, "a")]
    except Exception as e:
        print(f"Error extracting links from {url}: {e}")
        links = []
    finally:
        driver.quit()
    return links

# Function to extract abstracts from a URL
def get_abstract_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        abstract_section = soup.find(text=lambda text: text and "abstract" in text.lower())
        if abstract_section:
            parent = abstract_section.find_parent(["div", "p", "section", "article"])
            if parent:
                return parent.get_text(strip=True).split('title')[0].strip()
        return "Abstract not found."
    except Exception as e:
        print(f"Error retrieving abstract from {url}: {e}")
        return "Abstract could not be retrieved."

# Process CSV to extract and summarize abstracts
def process_csv(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    results = []
    for index, row in df.iterrows():
        url = row.get("url")
        if url:
            print(f"Processing URL: {url}")
            links = get_clickable_links(url)
            for link in links:
                print(f"Extracting abstract from: {link}")
                abstract = get_abstract_from_url(link)
                summary = summarize_with_bart(abstract)
                results.append({"Original_URL": url, "Link": link, "Abstract": abstract, "Summary": summary})
    
    # Save results to a CSV
    output_df = pd.DataFrame(results)
    output_df.to_csv(output_csv, index=False)
    print(f"Results saved to {output_csv}")

# Example Usage
if __name__ == "__main__":
    input_csv = "Top_Cited_Publications_With_URLs1.csv"
    output_csv = "extracted_and_summarized_links.csv"
    process_csv(input_csv, output_csv)
