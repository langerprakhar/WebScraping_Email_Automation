import pandas as pd
import requests

# Load the CSV file containing links
input_file = "Top_Cited_Publications_With_URLs.csv"  # Replace with your input file
output_file = "url_with_html.csv"  # Output file to save updated data

# Read the CSV file
df = pd.read_csv(input_file)

# Ensure there is a column named 'link'
if 'url' not in df.columns:
    raise ValueError("The CSV file must contain a 'link' column with URLs.")

# Add a new column to store the HTML structure
df['html_structure'] = None

# Iterate through the links and fetch the HTML structure
for index, row in df.iterrows():
    url = row['url']
    if pd.notna(url):
        try:
            # Fetch the HTML content of the URL
            response = requests.get(url, timeout=10)  # Adjust timeout as needed
            response.raise_for_status()  # Raise an error for bad responses
            df.at[index, 'html_structure'] = response.text
        except requests.RequestException as e:
            print(f"Failed to fetch {url}: {e}")
            df.at[index, 'html_structure'] = "Failed"

# Save the updated DataFrame to a new CSV
df.to_csv(output_file, index=False)
print(f"Updated CSV saved to {output_file}")
