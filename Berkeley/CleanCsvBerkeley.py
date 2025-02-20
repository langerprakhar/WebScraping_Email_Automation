import csv
import re

# Input and output CSV file paths
input_file = "BerkeleyFaculty.csv"
output_file = "BerkeleyFaculty_Cleaned.csv"

# Regular expression to match email addresses
email_regex = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

# Function to extract a valid email from a string
def extract_email(text):
    match = re.search(email_regex, text)
    return match.group(0) if match else ""

# Read, clean, and write the CSV
with open(input_file, mode="r", encoding="utf-8") as infile, \
     open(output_file, mode="w", newline="", encoding="utf-8") as outfile:
    
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Read and write the header
    header = next(reader)
    writer.writerow(header)

    # Process each row
    for row in reader:
        # Assuming the "Email" column is the second column (index 1)
        row[1] = extract_email(row[1])  # Extract valid email
        writer.writerow(row)

print(f"Email column cleaned. Output saved to {output_file}.")
