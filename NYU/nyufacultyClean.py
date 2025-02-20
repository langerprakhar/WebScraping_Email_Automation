import csv
import re

# Input and output file paths
input_csv = "nyu_faculty.csv"
output_csv = "nyu_faculty_cleaned.csv"

# Function to process each professor's details
def process_details(details):
    # Split the details into lines
    lines = details.split("\n")
    email = ""
    description = ""
    research_area = ""

    for line in lines:
        line = line.strip()
        # Check for email line
        if "Email:" in line:
            email_match = re.search(r"Email:\s*(.*)", line)
            if email_match:
                email = email_match.group(1).replace(" at ", "@").replace(" ", "")
        # Check for lines starting with "Office" or "Ext" to ignore
        elif line.startswith("Office") or line.startswith("Ext"):
            continue
        # Add to research area or description based on position of email
        elif email == "":
            description += line + " "
        else:
            research_area += line + " "

    # Clean and return the extracted details
    return description.strip(), email.strip(), research_area.strip()

# Read the input CSV, process data, and write to the output CSV
with open(input_csv, mode="r", encoding="utf-8") as infile, open(output_csv, mode="w", newline="", encoding="utf-8") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Write the header row
    writer.writerow(["Name", "Description", "Email", "Research Area"])

    # Skip the header row in the input file
    next(reader)

    # Process each row in the input file
    for row in reader:
        name, details = row
        description, email, research_area = process_details(details)
        writer.writerow([name, description, email, research_area])

print(f"Data cleaned and saved to {output_csv}")
