import pandas as pd
from bs4 import BeautifulSoup

# Read the HTML content from the file
with open("ICL.html", 'r', encoding='utf-8') as file:
    html_content = file.read()

# Initialize BeautifulSoup to parse the HTML
soup = BeautifulSoup(html_content, 'html.parser')

# List to store faculty data
faculty_data = []

# Find all the professor blocks using the <h3 class="sr-only"> tag (or a similar identifying tag)
professors = soup.find_all('h3', class_='sr-only')

# Iterate over each professor entry
for professor in professors:
    try:
        # Find the corresponding name inside <div class="name-wrapper">
        name_wrapper = professor.find_next('div', class_='name-wrapper')
        if name_wrapper:
            name_elem = name_wrapper.find('span', class_='person-name')
            name = name_elem.text.strip() if name_elem else 'Not Available'
        else:
            name = 'Not Available'

        # Extract email from <p class="contact">
        contact_elem = professor.find_next('p', class_='contact')
        if contact_elem:
            email_elem = contact_elem.find('a', class_='email')
            email = email_elem['href'].replace('mailto:', '').strip() if email_elem else 'Not Available'
        else:
            email = 'Not Available'

        # Extract research interests (next <div class="dept-wrapper"> and <p> inside it)
        dept_wrapper = professor.find_next('div', class_='dept-wrapper')
        if dept_wrapper:
            research_area_elem = dept_wrapper.find('p')
            research_area = research_area_elem.text.strip() if research_area_elem else 'Not Available'
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
df.to_csv('faculty_data.csv', index=False)
print("Data saved to 'faculty_data.csv'")
