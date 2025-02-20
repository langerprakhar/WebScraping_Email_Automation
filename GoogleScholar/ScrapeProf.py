from scholarly import scholarly

# Search for the author
search_query = scholarly.search_author('Alan Blackwell')
author = next(search_query)

# Fill author details (includes publications)
author = scholarly.fill(author)

# Fetch publications
publications = author.get('publications', [])

# Get title and description for each publication
for pub in publications:
    scholarly.fill(pub)  # Fill publication details
    title = pub['bib'].get('title', 'No title available')
    description = pub['bib'].get('abstract', 'No description available')
    print(f"Title: {title}")
    print(f"Description: {description}")
    print("-" * 40)
