import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_cornell_cs_faculty(url):
    try:
        # Add headers to mimic browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }

        # Fetch webpage content
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Initialize list to store faculty data
        faculty_data = []

        # Locate all blocks containing professor information
        professor_blocks = soup.find_all('div', class_='person-listing')

        for block in professor_blocks:
            # Extract name
            name_block = block.find('div', class_='text-primary')
            name = name_block.get_text(strip=True) if name_block else 'Not Available'

            # Extract research areas
            research_area_block = block.find('span', class_='inline-field')
            research_area = research_area_block.find('a').get_text(strip=True) if research_area_block and research_area_block.find('a') else 'Not Available'

            # Extract email
            email_block = block.find('span', class_='field-content')
            email = email_block.find('a').get_text(strip=True) if email_block and email_block.find('a') else 'Not Available'

            # Combine data into a dictionary
            faculty_entry = {
                'Name': name,
                'Research Area': research_area,
                'Email': email
            }

            # Add to the list if not all fields are empty
            if any(value != 'Not Available' for value in faculty_entry.values()):
                faculty_data.append(faculty_entry)

        # Remove duplicates based on Name and Email
        df = pd.DataFrame(faculty_data)
        df.drop_duplicates(subset=['Name', 'Email'], inplace=True)

        # Save the data to a CSV file
        df.to_csv('cornell_cs_faculty.csv', index=False)
        print("Data saved to 'cornell_cs_faculty.csv'")

    except Exception as e:
        print(f"An error occurred: {e}")

# URL of the Cornell CS faculty page
faculty_url = "https://www.cs.cornell.edu/people/faculty"
scrape_cornell_cs_faculty(faculty_url)
