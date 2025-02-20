import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_research_areas(url):
    """
    Scrapes research areas from the specified URL and generates abbreviations.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Locate the div with the specified class
        research_area_div = soup.find('div', class_='facetwp-facet facetwp-facet-research facetwp-type-fselect')
        if not research_area_div:
            print("No research areas found.")
            return {}

        # Extract the research areas
        research_areas = [area.text.strip() for area in research_area_div.find_all('option') if area.text.strip()]
        
        # Generate abbreviations
        abbreviations = {area: ''.join(word[0].upper() for word in area.split() if word).strip() for area in research_areas}
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
            matches[['Name', 'Email', 'Research Area']].to_csv('matchedProfs.csv', index=False)
            print("Results saved to matchedProfs.csv.")
        else:
            print("No professors found with the given interests.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
faculty_url = "https://www.eecs.mit.edu/role/faculty/"  # Replace with the actual URL containing the research areas
csv_file_path = 'mit_eecs_faculty_final.csv'

# Step 1: Define the research areas list and display them
research_areas_list = [
    "AI and Society",
    "AI for Healthcare and Life Sciences",
    "Artificial Intelligence + Machine Learning",
    "Biological and Medical Devices and Systems",
    "Communications Systems",
    "Computational Fabrication and Manufacturing",
    "Computer Architecture",
    "Educational Technology",
    "Electronic, Magnetic, Optical and Quantum Materials and Devices",
    "Energy",
    "Graphics and Vision",
    "Human-Computer Interaction",
    "Information Science and Systems",
    "Integrated Circuits and Systems",
    "Nanoscale Materials, Devices, and Systems",
    "Natural Language and Speech Processing",
    "Optics + Photonics",
    "Optimization and Game Theory",
    "Programming Languages and Software Engineering",
    "Quantum Computing, Communication, and Sensing",
    "Robotics",
    "Security and Cryptography",
    "Signal Processing",
    "Systems Theory, Control, and Autonomy",
    "Systems and Networking",
    "Theory of Computation"
]

# Display the research areas list
print("Total Unique Research Areas:", len(research_areas_list))
for idx, area in enumerate(research_areas_list, 1):
    print(f"{idx}. {area}")

# Step 2: Scrape research areas and generate abbreviations
research_area_abbreviations = scrape_research_areas(faculty_url)

# Step 3: Input user interests and filter professors
user_interest = input("Enter your research areas of interest (e.g., Vision, Robotics): ")
filter_professors_by_interest(csv_file_path, user_interest, research_area_abbreviations)
