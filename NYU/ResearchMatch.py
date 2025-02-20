import pandas as pd

# Function to display unique research areas and filter professors based on user input
def filter_professors_by_interest(csv_file, interest_input):
    """
    Displays unique research areas and filters professors based on user input and available research areas.
    Ensures professors have *all* specified interests.
    """
    try:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(csv_file)

        # Extract the 'Research Area' column and split by commas to get individual research areas
        all_research_areas = df['Research Area'].dropna().apply(lambda x: x.split(',')).explode().str.strip()

        # Ensure uniqueness of research areas across all rows
        unique_research_areas = sorted(set(all_research_areas))

        # Display the unique research areas list
        print("Total Unique Research Areas in CSV:", len(unique_research_areas))
        for idx, area in enumerate(unique_research_areas, 1):
            print(f"{idx}. {area}")

        # Prompt the user for their research areas of interest after displaying the options
        user_interest = input("\nEnter your research areas of interest: ")

        # Expand user input based on their interest
        interests = [area.strip().upper() for area in user_interest.split(",")]

        # Filter professors whose research area contains *all* of the interests
        mask = pd.Series([True] * len(df))  # Initialize mask as True for all rows
        for interest in interests:
            mask &= df['Research Area'].str.contains(interest, case=False, na=False)

        # Display and save the matching professors
        matches = df[mask]
        if not matches.empty:
            print("Matching Professors found. Saving to CSV...")
            # Save the matching rows to a new CSV file
            matches[['Name','Description','Email', 'Research Area']].to_csv('nyu_matchedProfs.csv', index=False)
            print("Results saved to nyu_matchedProfs.csv.")
        else:
            print("No professors found with the given interests.")

    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
csv_file_path = 'nyu_faculty_cleaned.csv'  # Adjust to your actual CSV file path

# Call the function to display the research areas and then filter based on user input
filter_professors_by_interest(csv_file_path, None)
