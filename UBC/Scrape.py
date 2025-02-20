import pandas as pd
from bs4 import BeautifulSoup

# Read the HTML content from the file
with open("UBC.html", 'r', encoding='utf-8') as file:
    html_content = file.read()

# Initialize BeautifulSoup to parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')

# List to store faculty data
faculty_data = []

# Find all rows containing professor information
professors = soup.find_all('tr')  # Assuming professor data is in table rows

# Iterate over each professor entry
for professor in professors:
    try:
        # Extract the name
        name_td = professor.find('td', class_="views-field views-field-field-person-lname is-active views-field-field-person-hp views-field-field-person-google-scholar")
        if name_td:
            name_elem = name_td.find('a', class_='contact-content-name')
            name = name_elem.text.strip() if name_elem else 'Not Available'
        else:
            name = 'Not Available'

        # Extract the email
        email_td = professor.find('td', class_="views-field views-field-field-person-job-title views-field-field-person-email views-field-field-person-building views-field-field-person-office-phone views-field-field-person-status")
        if email_td:
            email_elem = email_td.find('a')  # Email is in <a> tag
            email = email_elem.text.strip() if email_elem else 'Not Available'
        else:
            email = 'Not Available'

        # Extract research areas
        research_td = professor.find('td', class_="views-field views-field-field-research-groups views-field-field-research-interests-1")
        if research_td:
            # Get all text, including clickable links
            research_areas = []
            for content in research_td.contents:
                if content.name == 'a':  # If it's a clickable link
                    research_areas.append(content.text.strip())
                elif isinstance(content, str):  # If it's plain text
                    research_areas.append(content.strip())
            research_area = ','.join(filter(None, research_areas))
        else:
            research_area = 'Not Available'

        # Append the data for each professor
        faculty_data.append({
            'Name': name,
            'Email': email,
            'Research Area': research_area
        })

    except Exception as e:
        print(f"Error processing a professor: {e}")
        continue

# Convert the list to a pandas DataFrame
df = pd.DataFrame(faculty_data)

# Save the data to a CSV file
df.to_csv('UBC_Faculty.csv', index=False)
print("Data saved to 'UBC_Faculty.csv'")
