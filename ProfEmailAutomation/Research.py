import pandas as pd
import re

def get_unique_research_areas(csv_filename):
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_filename)

        # Extract the "Research Area" column and remove NaN values
        research_areas = df['Research Area'].dropna()  

        # Split research areas by newline (if multiple areas are in a single cell)
        all_areas = []
        for area in research_areas:
            areas = area.split("\n")
            all_areas.extend([a.strip() for a in areas if a.strip()])

        # Filter out entries that contain numbers, special characters, or irrelevant metadata
        filtered_areas = [
            area for area in all_areas 
            if not re.search(r'\d', area)  # Remove if contains digits
            and not area.startswith(('(', ',', '_'))  # Remove if starts with special characters like parentheses, commas, underscores
            and area.lower() not in ['post-tenure', '[cs]']  # Remove known irrelevant terms
        ]

        # Get the unique research areas
        unique_areas = set(filtered_areas)

        # Return sorted unique research areas
        return sorted(unique_areas)

    except Exception as e:
        print(f"An error occurred while extracting unique research areas: {e}")

# Example usage
csv_file = 'mit_eecs_faculty_final.csv'  # Path to the CSV file containing the faculty data
unique_research_areas = get_unique_research_areas(csv_file)

# Print unique research areas
print("Unique Research Areas:")
for idx, area in enumerate(unique_research_areas, 1):
    print(f"{idx}. {area}")
