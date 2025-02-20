import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def scrape_princeton_cs_faculty(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        faculty_data = []

        professor_blocks = soup.find_all('div', class_='person clearfix')

        for block in professor_blocks:
            name = block.find('h2').get_text(strip=True) if block.find('h2') else 'Not Available'
            person_details = block.find('div', class_='person-details')
            address_details = block.find('div', class_='person-address')

            description = 'Not Available'
            research_area = 'Not Available'
            email = 'Not Available'

            if person_details:
                details_text = person_details.get_text(separator="\n").strip()
                parts = details_text.split("Research Interests")

                description = parts[0].strip() if len(parts) > 0 else 'Not Available'
                research_area = parts[1].strip() if len(parts) > 1 else 'Not Available'

                # Remove Homepage, Profile, and any unwanted characters
                description = re.sub(r'(Homepage|Profile)', '', description).strip()

                # Remove any content starting with '(' and followed immediately by numbers
                description = re.sub(r'^\(\d.*', '', description).strip()

                # Remove numbers or any text starting with '(' (including phone numbers and such)
                description = re.sub(r'\(.*\d.*', '', description).strip()

                description = re.sub(r'\s+\(', '(', description).strip()
                description = re.sub(r'\s+', ' ', description).strip()

                # Handle email correctly and remove unwanted parts
                email_match = re.search(r'\S+@[\w.]+\.edu', description)
                if email_match:
                    email = email_match.group(0)
                    description = description.replace(email, '').strip()

                # Remove any stray parentheses
                description = re.sub(r'\)', '', description).strip()

            if address_details:
                address_text = address_details.get_text(separator="\n").strip()
                address_text = re.sub(r'^\) .*', '', address_text).strip()  # Remove anything starting with ')'

                email_match = re.search(r'\S+@[\w.]+\.edu', address_text)
                if email_match and email == 'Not Available':
                    email = email_match.group(0)

            faculty_entry = {
                'Name': name,
                'Description': description,
                'Research Area': research_area,
                'Email': email
            }

            faculty_data.append(faculty_entry)

        df = pd.DataFrame(faculty_data)
        df.to_csv('princeton_cs_faculty_clean.csv', index=False)
        print("Data saved to 'princeton_cs_faculty_clean.csv'")

    except Exception as e:
        print(f"An error occurred: {e}")

faculty_url = "https://www.cs.princeton.edu/people/faculty"
scrape_princeton_cs_faculty(faculty_url)
