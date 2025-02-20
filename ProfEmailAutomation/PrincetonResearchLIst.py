import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_research_areas(url):
    """
    Scrapes research areas from the specified URL by extracting headers (clickable links) 
    inside <a> tags that are nested within <h3> elements with class 'research-area-title'.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Locate the elements with the class 'research-area'
        research_area_divs = soup.find_all('div', class_='research-area')
        if not research_area_divs:
            print("No research areas found.")
            return {}

        # Extract the research areas from <a> tags within <h3> elements with class 'research-area-title'
        research_areas = []
        for div in research_area_divs:
            h3_tag = div.find('h3', class_='research-area-title')  # Find <h3> with the class 'research-area-title'
            if h3_tag:
                link = h3_tag.find('a')  # Find the <a> tag within the <h3> tag
                if link and link.get_text(strip=True):  # Ensure there's text inside the <a> tag
                    research_areas.append(link.get_text(strip=True))

        # Remove duplicates
        research_areas = list(set(research_areas))

        # Generate abbreviations
        abbreviations = {area.upper(): ''.join(word[0].upper() for word in area.split()) for area in research_areas}
        return abbreviations

    except Exception as e:
        print(f"An error occurred while scraping research areas: {e}")
        return {}

def filter_professors_by_interest(csv_file, interest_input, abbreviations):
    """
    Filters professors from the CSV file based on user interest and available abbreviations.
    Ensures professors have *all* specified interests.
    """
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(csv_file)

        # Expand user input based on abbreviations and create a list of all interests
        interests = [abbreviations.get(area.strip().upper(), area.strip()) for area in interest_input.split(",")]

        # Filter professors whose research area contains *all* of the interests
        mask = pd.Series([True] * len(df))  # Initialize mask as True for all rows
        for interest in interests:
            mask &= df['Research Area'].str.contains(interest, case=False, na=False)

        # Display and save the matching professors
        matches = df[mask]
        if not matches.empty:
            print("Matching Professors found. Saving to CSV...")
            # Save the matching rows to a new CSV file
            matches[['Name', 'Email', 'Research Area']].to_csv('Princeton_matchedProfs.csv', index=False)
            print("Results saved to Princeton_matchedProfs.csv.")
        else:
            print("No professors found with the given interests.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
faculty_url = "https://www.cs.princeton.edu/research/areas"  # Replace with the actual URL containing the research areas
csv_file_path = 'princeton_cs_faculty_clean.csv'

# Step 1: Define the research areas list and display them
research_areas_list = [
    "Computational Biology",
    "Computer Architecture",
    "Economics & Computation",
    "Human-Computer Interaction",
    "Machine Learning",
    "Natural Language Processing",
    "Programming Languages & Compilers",
    "Public Law & Policy",
    "Robotics",
    "Security & Privacy",
    "Systems & Networking",
    "Theory",
    "Vision & Graphics"
]

# Display the research areas list
print("Total Unique Research Areas:", len(research_areas_list))
for idx, area in enumerate(research_areas_list, 1):
    print(f"{idx}. {area}")

# Step 2: Scrape research areas and generate abbreviations
research_area_abbreviations = scrape_research_areas(faculty_url)

# Print abbreviations for debugging
print("Extracted Research Areas and Abbreviations:", research_area_abbreviations)

# Step 3: Input user interests and filter professors
user_interest = input("Enter your research areas of interest (e.g., Vision, Robotics): ")
filter_professors_by_interest(csv_file_path, user_interest, research_area_abbreviations)
