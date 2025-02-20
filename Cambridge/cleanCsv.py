import pandas as pd
import re

# Function to clean and separate concatenated email addresses
def clean_email(email, professor_name=None):
    """
    Clean and separate concatenated email addresses by:
    - Recognizing valid email patterns
    - Handling concatenated emails separated by periods
    - Replacing placeholders (e.g., first.name, at, dot)
    """
    if not isinstance(email, str):  # Ensure email is a string before processing
        return 'Not Available'
    
    # Regex to match valid email addresses
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
    # Find all valid emails in the string
    emails = re.findall(email_pattern, email)
    
    # Clean each email individually
    cleaned_emails = []
    for e in emails:
        # Replace ' DOT ' and ' AT ' with appropriate symbols
        e = re.sub(r'\s*DOT\s*', '.', e)
        e = re.sub(r'\s*AT\s*', '@', e)

        # Replace ' at ' with '@' and ' dot ' with '.'
        e = re.sub(r'\s*at\s*', '@', e)
        e = re.sub(r'\s*dot\s*', '.', e)

        # Replace spaces in the domain with dots
        e = re.sub(r'\s+', '.', e)

        # Add cleaned email to the list
        cleaned_emails.append(e)
    
    # Join cleaned emails with a comma
    email = ', '.join(cleaned_emails)
    
    # If professor_name is provided, replace placeholders [first.name] and [last.name]
    if professor_name:
        # Remove any title (e.g., "Dr", "Prof") and split the name into first and last
        name_parts = professor_name.split()
        
        # The first name is always the second part if title exists, else the first part
        first_name = name_parts[1] if len(name_parts) > 1 and name_parts[0].lower() in ['dr', 'prof'] else name_parts[0]
        last_name = name_parts[-1]  # Last part is always the last name
        
        # Replace any placeholder variations in the email with the professor's first and last name
        email = re.sub(r'first\.?name|firstname', first_name, email, flags=re.IGNORECASE)
        email = re.sub(r'last\.?name|lastname', last_name, email, flags=re.IGNORECASE)
    
    return email

# Read the CSV file containing the scraped data
df = pd.read_csv('cambridge_faculty.csv')

# Function to clean and process each row
def process_row(row):
    professor_name = row['Name']
    email = row['Email']

    # Clean the email address and handle placeholders
    cleaned_email = clean_email(email, professor_name)

    # Update the row with the cleaned email
    row['Email'] = cleaned_email
    return row

# Apply the process_row function to each row in the DataFrame
df = df.apply(process_row, axis=1)

# Save the cleaned DataFrame back to CSV
df.to_csv('cambridge_faculty_cleaned2.csv', index=False)
print("Data saved to 'cambridge_faculty_cleaned2.csv'")
