import pandas as pd
from scholarly import scholarly

def get_publication_urls(publication):
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
    # Read professor data from CSV
    df = pd.read_csv(file_path)
    
    # Validate required columns
    if not {'Name', 'Research Interests'}.issubset(df.columns):
        raise ValueError("CSV file must contain 'Name' and 'Research Interests' columns.")
    
    print(f"Successfully loaded CSV file with {len(df)} professors.")
    
    # Initialize dictionary to store publications
    relevant_publications = {}

    # Process each professor
    for _, row in df.iterrows():
        professor_name = row['Name']
        research_area = row['Research Interests']
        print(f"\nProcessing professor: {professor_name} with research area: {research_area}")
        
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
                    # Get the URL for the publication
                    pub_url = get_publication_urls(pub)
                    filtered_pubs.append({
                        "title": pub["bib"].get("title"),
                        "year": year,
                        "citations": pub["num_citations"],
                        "research_area": research_area,
                        "url": pub_url
                    })
            
            # Sort publications first by citation count (descending), then by year (descending)
            filtered_pubs.sort(key=lambda x: (x['citations'], x['year']), reverse=True)

            # Save filtered publications
            relevant_publications[professor_name] = filtered_pubs
            
            if filtered_pubs:
                print(f"Top publications for {professor_name}:")
                for pub in filtered_pubs[:3]:  # Print top 3 publications
                    print(f"- {pub['title']} ({pub['year']}) | Citations: {pub['citations']} | URL: {pub['url']}")
            else:
                print(f"No relevant publications found for {professor_name} within the specified year range.")
        
        except Exception as e:
            print(f"Error processing professor {professor_name}: {e}")
    
    return relevant_publications


# Example Usage
if __name__ == "__main__":
    file_path = "Filtered_Professors_Artificial_Intelligence.csv"  # Replace with the path to your CSV file
    start_year = 2022
    end_year = 2024

    publications = get_most_cited_recent_publications_from_csv(file_path, start_year, end_year)

    # Display results
    print("\nFinal List of Publications with URLs:")
    for professor, pubs in publications.items():
        print(f"\nProfessor: {professor}")
        if pubs:
            for pub in pubs:
                print(f"- {pub['title']} ({pub['year']}) | Citations: {pub['citations']} | Area: {pub['research_area']} | URL: {pub['url']}")
        else:
            print("No relevant publications found.")
