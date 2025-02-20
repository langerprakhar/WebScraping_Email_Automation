import pandas as pd
import re

# Load the CSV into a DataFrame
input_file = 'UBC_Faculty.csv'  # Replace with your input file name
output_file = 'cleaned_UBC_Faculty.csv'  # Replace with your desired output file name

# Read the CSV
df = pd.read_csv(input_file)

# Function to clean up duplicate commas in a string
def clean_commas(text):
    if isinstance(text, str):  # Only process strings
        return re.sub(r',\s*,+', ',', text)
    return text

# Apply the cleaning function to all cells in the DataFrame
df = df.applymap(clean_commas)

# Save the cleaned DataFrame to a new CSV
df.to_csv(output_file, index=False)
print(f"Cleaned data saved to '{output_file}'")
