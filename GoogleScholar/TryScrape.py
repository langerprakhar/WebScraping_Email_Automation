from scholarly import scholarly

# Define the keyword or label to search for
label = "machine learning"  # Replace with your desired label/keyword

# Use search_author to find researchers by name or keyword
search_query = scholarly.search_author(label)

# Fetch and print researcher details, including email domains
print(f"Researchers associated with '{label}':\n")
for i in range(10):  # Limit to the first 10 results
    try:
        author = next(search_query)
        print(f"Name: {author['name']}")
        print(f"Affiliation: {author['affiliation']}")
        print(f"Email Domain: {author.get('email_domain', 'Not Available')}")
        print(f"Interests: {', '.join(author.get('interests', []))}")
        print("-" * 40)
    except StopIteration:
        print("No more results available.")
        break
