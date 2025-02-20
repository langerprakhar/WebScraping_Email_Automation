import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_mit_cs_faculty(url):
    try:
        # Add headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }

        # Fetch webpage content
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Initialize list for storing professor data
        professor_data = []

        # Find all blocks with professor details
        professor_blocks = soup.find_all('div', class_='people-research')

        for block in professor_blocks:
            # Extract professor name
            name = block.find('h3').text.strip() if block.find('h3') else 'Not Available'

            # Extract email (if present)
            email_tag = block.find('a', href=True)
            email = email_tag.text.strip() if email_tag and '@' in email_tag.text else 'Not Available'

            # Extract subjects of interest
            subjects_tag = block.find_all('div', class_='field-content')
            subjects = ', '.join(tag.text.strip() for tag in subjects_tag if tag.text.strip())

            # Add data to the list
            professor_data.append({
                'Name': name,
                'Email': email,
                'Subjects of Interest': subjects
            })

        # Save data to a CSV file
        df = pd.DataFrame(professor_data)
        df.to_csv('mit_cs_faculty.csv', index=False)
        print("Data saved to 'mit_cs_faculty.csv'")

    except Exception as e:
        print(f"An error occurred: {e}")

# URL for MIT CS faculty
faculty_url = "https://www.eecs.mit.edu/role/faculty/"
scrape_mit_cs_faculty(faculty_url)
