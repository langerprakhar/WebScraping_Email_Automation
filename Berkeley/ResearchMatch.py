import pandas as pd
from fuzzywuzzy import fuzz

def extract_unique_research_areas_and_filter(csv_file):
    """
    Extracts unique research areas from the specified CSV file, generates abbreviations,
    and filters professors based on the desired research interest.
    """
    try:
        # Load the CSV file
        df = pd.read_csv(csv_file)

        # Debug: Print column names for inspection
        print("Columns in the CSV file:", df.columns)

        # Ensure "Research Interests" column exists
        if "Research Interests" not in df.columns:
            print("The 'Research Interests' column is missing in the CSV file.")
            return None

        # Extract all research areas, split if multiple are listed in one cell
        all_areas = df['Research Interests'].dropna().str.split(',').explode().str.strip()

        # Get unique research areas and sort them
        unique_areas = sorted(all_areas.unique())

        # Generate abbreviations for each research area
        abbreviations = {
            area: ''.join(word[0].upper() for word in area.split() if word).strip()
            for area in unique_areas
        }

        # Display unique research areas and their abbreviations
        print(f"Total Unique Research Areas: {len(unique_areas)}")
        for idx, area in enumerate(unique_areas, 1):
            print(f"{idx}. {area} ({abbreviations[area]})")

        # Ask user for a desired research interest
        desired_interest = input("\nEnter your desired research interest: ").strip()

        # Perform fuzzy matching
        threshold = 80  # Set a similarity threshold
        matched_rows = []

        for _, row in df.iterrows():
            research_interests = row['Research Interests']
            if isinstance(research_interests, str):  # Ensure it's a string
                score = fuzz.partial_ratio(research_interests.lower(), desired_interest.lower())
                if score >= threshold:
                    matched_rows.append(row)

        if matched_rows:
            # Create a DataFrame of matched rows
            matched_df = pd.DataFrame(matched_rows)

            # Save the filtered rows to a CSV file
            output_file = f"Filtered_Professors_{desired_interest.replace(' ', '_')}.csv"
            matched_df.to_csv(output_file, index=False)
            print(f"\nFiltered professors saved to '{output_file}'.")
        else:
            print("\nNo professors matched the desired research interest.")

        return unique_areas, abbreviations

    except FileNotFoundError:
        print(f"The file '{csv_file}' was not found. Please check the path.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
csv_file_path = 'BerkeleyFaculty_Cleaned.csv'  # Replace with the path to your CSV file
result = extract_unique_research_areas_and_filter(csv_file_path)
