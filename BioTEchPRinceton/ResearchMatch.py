import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_research_areas(url):
    """
    Scrapes research areas from the specified URL and generates a list of research areas.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Locate the div with the specified class for research areas
        research_area_divs = soup.find_all('div', class_='content-list-item-details')
        if not research_area_divs:
            print("No research areas found.")
            return []

        # Extract the research areas from the span elements
        research_areas = [area.find('span', class_='field field--name-title field--type-string field--label-hidden').text.strip()
                          for area in research_area_divs if area.find('span', class_='field field--name-title field--type-string field--label-hidden')]

        return research_areas

    except Exception as e:
        print(f"An error occurred while scraping research areas: {e}")
        return []

def filter_professors_by_interest(csv_file, interest_input):
    """
    Filters professors from the CSV file based on user input for research areas.
    Ensures professors have *all* specified interests.
    """
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(csv_file)

        # Expand user input into a list of interests
        interests = [area.strip() for area in interest_input.split(",")]

        # Filter professors whose research area contains *all* of the specified interests
        mask = pd.Series([True] * len(df))  # Initialize mask as True for all rows
        for interest in interests:
            mask &= df['Research Area'].str.contains(interest, case=False, na=False)

        # Display and save the matching professors
        matches = df[mask]
        if not matches.empty:
            print("Matching Professors found. Saving to CSV...")
            # Save the matching rows to a new CSV file
            matches[['Name', 'Email', 'Research Area']].to_csv('matchedProfs.csv', index=False)
            print("Results saved to matchedProfs.csv.")
        else:
            print("No professors found with the given interests.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
faculty_url = "https://molbio.princeton.edu/research-areas"  # URL containing the research areas
csv_file_path = 'princeton_faculty_all_data.csv'  # Path to your CSV file containing faculty data

# Step 1: Scrape research areas and print them
research_areas = scrape_research_areas(faculty_url)

# Print the research areas in an ordered format
print("Available Research Areas:")
for idx, area in enumerate(research_areas, 1):
    print(f"{idx}. {area}")

# Step 2: Input user interests and filter professors based on Research Area column in CSV
user_interest = input("Enter your research areas of interest (comma-separated, e.g., Vision, Robotics): ")
filter_professors_by_interest(csv_file_path, user_interest)
