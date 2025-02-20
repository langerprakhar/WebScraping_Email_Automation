import pandas as pd
import requests
from bs4 import BeautifulSoup

# Function to extract the first link from <h3> elements with class 'gs_rt'
def get_first_link_from_url(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the first <h3> element with the class 'gs_rt'
        first_element = soup.find('h3', class_='gs_rt')
        
        # Extract the href attribute from the <a> tag inside the <h3> element
        if first_element:
            a_tag = first_element.find('a')  # Find the <a> tag within the <h3> element
            if a_tag and a_tag.get('href'):  # Check if <a> tag exists and has 'href'
                return a_tag['href']  # Return the href
        return None  # Return None if no valid link is found
    
    except requests.exceptions.RequestException as e:
        print(f"Error accessing URL {url}: {e}")
        return None

# Function to process the CSV and extract the first link
def process_csv(input_csv, output_csv):
    # Read the input CSV
    df = pd.read_csv(input_csv)
    
    # Validate if 'url' column exists
    if 'url' not in df.columns:
        raise ValueError("Input CSV must contain a 'url' column.")
    
    # Initialize a list to store results
    extracted_links = []
    
    # Process each URL
    for index, row in df.iterrows():
        url = row['url']
        if pd.notna(url):
            print(f"Processing URL: {url}")
            first_link = get_first_link_from_url(url)
            extracted_links.append({
                "Original_URL": url,
                "Extracted_Link": first_link if first_link else "No link found"
            })
    
    # Create a DataFrame with extracted links and save to a CSV
    result_df = pd.DataFrame(extracted_links)
    result_df.to_csv(output_csv, index=False)
    print(f"Saved extracted links to {output_csv}")

# Example usage
if __name__ == "__main__":
    input_csv = "Top_Cited_Publications_With_URLs1.csv"  # Input CSV path
    output_csv = "extracted_first_links_45_123.csv"  # Output CSV path
    
    process_csv(input_csv, output_csv)
