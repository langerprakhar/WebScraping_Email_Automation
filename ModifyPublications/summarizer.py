from transformers import BartForConditionalGeneration, BartTokenizer
import pandas as pd
from scholarly import scholarly

# Load BART model and tokenizer
model_name = "facebook/bart-large-cnn"  # Fine-tuned for summarization
bart_model = BartForConditionalGeneration.from_pretrained(model_name)
bart_tokenizer = BartTokenizer.from_pretrained(model_name)

def summarize_with_bart(text):
    """
    Summarizes a given text using BART.
    """
    try:
        # Encode the input text
        inputs = bart_tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
        # Generate summary
        summary_ids = bart_model.generate(
            inputs, 
            max_length=200,  # Maximum length of summary
            min_length=50,   # Minimum length of summary
            length_penalty=2.0, 
            num_beams=4,     # Beam search for better results
            early_stopping=True
        )
        # Decode and return the summary
        summary = bart_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary
    except Exception as e:
        print(f"Error in summarizing with BART: {e}")
        return "Summary could not be generated."

def get_relevant_publications_with_summary(file_path, start_year, end_year):
    """
    Process the professors' data from a CSV, retrieve their publications,
    and summarize the top ones using BART.
    """
    # Read professor data from CSV
    df = pd.read_csv(file_path)
    
    # Validate required columns
    if not {'Name', 'Research Interests'}.issubset(df.columns):
        raise ValueError("CSV file must contain 'Name' and 'Research Interests' columns.")
    
    # Initialize dictionary to store publications and summaries
    relevant_publications = {}

    # Process each professor
    for _, row in df.iterrows():
        professor_name = row['Name']
        research_area = row['Research Interests'].strip()  # Research area from CSV
        print(f"\nProcessing professor: {professor_name} with research area: {research_area}")

        try:
            # Search for the professor on Google Scholar
            search_query = scholarly.search_author(professor_name)
            author = next(search_query)
            print(f"Found professor: {professor_name} on Google Scholar.")
            author_publications = scholarly.fill(author).get("publications", [])
            print(f"Found {len(author_publications)} publications for {professor_name}.")
            
            # Filter publications by year and citations
            filtered_pubs = []
            for pub in author_publications:
                title = pub["bib"].get("title", "")
                year = pub["bib"].get("pub_year")
                citations = pub.get("num_citations", 0)
                abstract = pub["bib"].get("abstract", "")
                if not abstract:
                    print(f"No abstract found for: {pub['title']}")

                # Check year range
                if year and start_year <= int(year) <= end_year:
                    # If abstract is available, use it for summarization; otherwise, use title
                    text_to_summarize = abstract if abstract else title
                    filtered_pubs.append({
                        "title": title,
                        "year": year,
                        "citations": citations,
                        "summary": None,  # Placeholder for the summary
                        "text_to_summarize": text_to_summarize  # Include abstract or title
                    })
            
            # Sort by citations (descending) to get the "top" publications
            filtered_pubs.sort(key=lambda x: x["citations"], reverse=True)

            # Summarize top publications
            for pub in filtered_pubs[:5]:  # Limit to top 5 publications
                print(f"Summarizing publication: {pub['title']}")
                pub['summary'] = summarize_with_bart(pub['text_to_summarize'])
            
            # Save filtered and summarized publications
            relevant_publications[professor_name] = filtered_pubs

        except Exception as e:
            print(f"Error processing professor {professor_name}: {e}")

    return relevant_publications


# Example Usage
if __name__ == "__main__":
    file_path = "Filtered_Professors_Artificial_Intelligence.csv"  # Path to your CSV
    start_year = 2022
    end_year = 2024

    # Get publications with summaries
    publications = get_relevant_publications_with_summary(file_path, start_year, end_year)

    # Display results
    for professor, pubs in publications.items():
        print(f"\nProfessor: {professor}")
        if pubs:
            for pub in pubs:
                print(f"- {pub['title']} ({pub['year']}) | Citations: {pub['citations']}")
                print(f"  Summary: {pub['summary']}")
        else:
            print("No relevant publications found.")
