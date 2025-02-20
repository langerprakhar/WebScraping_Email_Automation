import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_imperial_academic_staff(url):
    try:
        # Send a GET request to the website
        response = requests.get(url)
        
        # Parse the content of the webpage
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # List to store the extracted faculty data
        faculty_data = []
        
        # Find all the professor's divs
        professors = soup.find_all('div', class_='staff-item')
        
        for professor in professors:
            try:
                # Extract the name (text from <span class="person-name">)
                name_elem = professor.find('div', class_='name-wrapper')
                name = name_elem.find('span', class_='person-name').text.strip() if name_elem else 'Not Available'

                # Extract the email (href from <a class="contact">)
                email_elem = professor.find('p', class_='contact')
                email = email_elem.find('a')['href'] if email_elem else 'Not Available'

                # Extract the research interests (from <div class="dept-wrapper"> <p> inside it)
                research_area_elem = professor.find('div', class_='dept-wrapper')
                research_area = research_area_elem.find('p').text.strip() if research_area_elem else 'Not Available'

                # Append the data to the faculty list
                faculty_data.append({
                    'Name': name,
                    'Email': email,
                    'Research Area': research_area
                })

            except Exception as e:
                print(f"Error processing a professor: {e}")
                continue
        
        # Create a DataFrame from the collected data
        df = pd.DataFrame(faculty_data)
        
        # Save the data to a CSV file
        df.to_csv('imperial_faculty.csv', index=False)
        print("Data saved to 'imperial_faculty.csv'")

    except Exception as e:
        print(f"An error occurred: {e}")

# URL of the Imperial College Computer Science academic staff page
url = "https://www.imperial.ac.uk/computing/people/academic-staff/"

# Call the scraping function
scrape_imperial_academic_staff(url)
