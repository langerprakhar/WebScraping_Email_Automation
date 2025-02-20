import pandas as pd
from scholarly import scholarly

def get_most_cited_recent_publications_from_csv(file_path, start_year, end_year, output_file):
    # Read professor data from CSV
    df = pd.read_csv(file_path)
    
    # Validate required columns
    if 'Name' not in df.columns:
        raise ValueError("CSV file must contain a 'Name' column.")
    
    print(f"Successfully loaded CSV file with {len(df)} professors.")
    
    # Initialize list to store all publications data
    all_publications = []

    # Process each professor
    for _, row in df.iterrows():
        professor_name = row['Name']
        print(f"\nProcessing professor: {professor_name}")
        
        try:
            # Search for the professor
            search_query = scholarly.search_author(professor_name)
            author = next(search_query)
            print(f"Found professor: {professor_name} on Google Scholar.")
            
            author_publications = scholarly.fill(author).get("publications", [])
            print(f"Found {len(author_publications)} publications for {professor_name}.")
            
            # Filter publications by year
            filtered_pubs = []
            for pub in author_publications:
                year = pub["bib"].get("pub_year")
                
                # Check if year is within the given range
                if year and start_year <= int(year) <= end_year:
                    filtered_pubs.append({
                        "title": pub["bib"].get("title"),
                        "year": year,
                        "citations": pub["num_citations"],
                        "professor": professor_name
                    })
            
            # Sort publications first by citation count (descending), then by year (descending)
            filtered_pubs.sort(key=lambda x: (x['citations'], x['year']), reverse=True)

            # Append the filtered publications to the list
            all_publications.extend(filtered_pubs)

            if filtered_pubs:
                print(f"Top publications for {professor_name}:")
                for pub in filtered_pubs[:3]:  # Print top 3 publications
                    print(f"- {pub['title']} ({pub['year']}) | Citations: {pub['citations']}")
            else:
                print(f"No relevant publications found for {professor_name} within the specified year range.")
        
        except Exception as e:
            print(f"Error processing professor {professor_name}: {e}")
    
    # Append all collected data to the CSV file
    if all_publications:
        # Create a DataFrame from the collected publications
        publications_df = pd.DataFrame(all_publications)
        
        # Append data to CSV (if the file doesn't exist, it will create it with headers)
        publications_df.to_csv(output_file, mode='a', index=False, header=not pd.io.common.file_exists(output_file))
    
    print(f"Publication data has been saved to {output_file}.")

# Example Usage
if __name__ == "__main__":
    file_path = "faculty_data.csv"  # Replace with the path to your CSV file
    output_file = "ICLProfessors_Publications.csv"  # Output file for storing publication data
    start_year = 2022
    end_year = 2024

    get_most_cited_recent_publications_from_csv(file_path, start_year, end_year, output_file)
