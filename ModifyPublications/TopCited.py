import pandas as pd
from scholarly import scholarly

def get_publication_urls(publication):
    """Extracts the DOI or searches for the publication URL on Google Scholar."""
    # Try to extract the DOI from the publication
    doi = publication["bib"].get("DOI")
    if doi:
        # Construct the URL from the DOI if available
        url = f"https://doi.org/{doi}"
    else:
        # If DOI is not available, use the title to search for the paper on Google Scholar
        title = publication["bib"].get("title", "No title available")
        search_url = f"https://scholar.google.com/scholar?q={title.replace(' ', '+')}"
        url = search_url
    return url

def get_most_cited_recent_publications_from_csv(file_path, start_year, end_year):
    """Fetches the top-cited publications of professors and saves them in a CSV."""
    # Read professor data from CSV
    df = pd.read_csv(file_path)
    
    # Validate required columns
    if not {'Name', 'Research Interests'}.issubset(df.columns):
        raise ValueError("CSV file must contain 'Name' and 'Research Interests' columns.")
    
    print(f"Successfully loaded CSV file with {len(df)} professors.")
    
    # Initialize list to store publication data
    all_publications = []

    # Process each professor
    for _, row in df.iterrows():
        professor_name = row['Name']
        research_area = row['Research Interests']
        print(f"\nProcessing professor: {professor_name} with research area: {research_area}")
        
        try:
            # Search for the professor on Google Scholar
            search_query = scholarly.search_author(professor_name)
            author = next(search_query)
            print(f"Found professor: {professor_name} on Google Scholar.")
            
            author_publications = scholarly.fill(author).get("publications", [])
            print(f"Found {len(author_publications)} publications for {professor_name}.")
            
            # Filter publications by year and get their URLs
            filtered_pubs = []
            for pub in author_publications:
                year = pub["bib"].get("pub_year")
                
                # Check if the publication's year is within the given range
                if year and start_year <= int(year) <= end_year:
                    # Get the publication URL
                    pub_url = get_publication_urls(pub)
                    filtered_pubs.append({
                        "professor_name": professor_name,
                        "title": pub["bib"].get("title"),
                        "year": year,
                        "citations": pub["num_citations"],
                        "research_area": research_area,
                        "url": pub_url
                    })
            
            # Sort publications by citation count (descending), then by year (descending)
            filtered_pubs.sort(key=lambda x: (x['citations'], x['year']), reverse=True)

            # Add top publications to the list (top 3 for each professor)
            all_publications.extend(filtered_pubs[:3])
            
            if filtered_pubs:
                print(f"Top publications for {professor_name}:")
                for pub in filtered_pubs[:3]:  # Print top 3 publications
                    print(f"- {pub['title']} ({pub['year']}) | Citations: {pub['citations']} | URL: {pub['url']}")
            else:
                print(f"No relevant publications found for {professor_name} within the specified year range.")
        
        except Exception as e:
            print(f"Error processing professor {professor_name}: {e}")
    
    # Save publications to CSV
    publications_df = pd.DataFrame(all_publications)
    if not publications_df.empty:
        publications_df.to_csv("Top_Cited_Publications_With_URLs.csv", index=False)
        print("\nSaved publications to 'Top_Cited_Publications_With_URLs.csv'")
    else:
        print("\nNo relevant publications to save.")
    
    return all_publications


# Example Usage
if __name__ == "__main__":
    file_path = "Filtered_Professors_Artificial_Intelligence.csv"  # Replace with the path to your CSV file
    start_year = 2022
    end_year = 2024

    publications = get_most_cited_recent_publications_from_csv(file_path, start_year, end_year)


