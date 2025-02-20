import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_mit_eecs_faculty(url):
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
        professor_blocks = soup.find_all('div', class_='people-entry small-12 medium-6 large-4 larger-3 cell')

        for block in professor_blocks:
            # Extract and clean data
            full_text = block.get_text(separator="\n").strip() if block else 'Not Available'

            # Split the text into lines
            lines = [line.strip() for line in full_text.split("\n") if line.strip()]
            name = lines[0] if len(lines) > 0 else 'Not Available'
            description = lines[1] if len(lines) > 1 else 'Not Available'
            email = next((line for line in lines if "@" in line), 'Not Available')
            
            # Research areas: remaining lines excluding known fields
            research_areas = [
                line for line in lines
                if line not in {name, description, email} and not line.startswith(("Office:", "(617)"))
            ]
            research_area_str = "\n".join(research_areas)

            # Combine data
            faculty_entry = {
                'Name': name,
                'Description': description,
                'Email': email,
                'Research Area': research_area_str
            }

            # Add to the list
            faculty_data.append(faculty_entry)

        # Save the data to a CSV file
        df = pd.DataFrame(faculty_data)
        df.to_csv('mit_eecs_faculty_final.csv', index=False)
        print("Data saved to 'mit_eecs_faculty_final.csv'")

    except Exception as e:
        print(f"An error occurred: {e}")

# URL of the MIT EECS faculty page
faculty_url = "https://www.eecs.mit.edu/role/faculty/"
scrape_mit_eecs_faculty(faculty_url)
