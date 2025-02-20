from bs4 import BeautifulSoup
import requests
import csv

# List of website URLs with university names
websites = [
    {"name": "MIT", "url": "https://www.eecs.mit.edu/people/faculty-advisors"},
    {"name": "Stanford University", "url": "https://cs.stanford.edu/directory/faculty"},
    {"name": "Carnegie Mellon University", "url": "https://www.cs.cmu.edu/directory"},
    {"name": "Harvard University", "url": "https://seas.harvard.edu/faculty"},
    {"name": "UC Berkeley", "url": "https://www.cs.berkeley.edu/people/faculty"},
    {"name": "University of Oxford", "url": "https://www.cs.ox.ac.uk/contacts"},
    {"name": "University of Cambridge", "url": "https://www.cam.ac.uk/about-us/contacts"},
    {"name": "Caltech", "url": "https://www.caltech.edu/academics/faculty"},
    {"name": "Yale University", "url": "https://www.cs.yale.edu/faculty"},
    {"name": "Princeton University", "url": "https://www.princeton.edu/academics/departments/cs"},
    {"name": "University of Washington", "url": "https://www.washington.edu/people/faculty"},
    {"name": "University of Chicago", "url": "https://cs.uchicago.edu/people/faculty"},
    {"name": "Tsinghua University", "url": "https://www.tsinghua.edu.cn/en/Academics/Departments/Faculty"},
    {"name": "ETH Zurich", "url": "https://www.ethz.ch/en/people.html"},
    {"name": "Imperial College London", "url": "https://www.imperial.ac.uk/computing/people"},
    {"name": "National University of Singapore", "url": "https://www.nus.edu.sg/our-people"},
    {"name": "Technical University of Munich", "url": "https://www.tum.de/en/about-tum/contact/faculty"},
    {"name": "EPFL", "url": "https://people.epfl.ch/cgi-bin/search"},
    {"name": "University of Tokyo", "url": "https://www.u-tokyo.ac.jp/en/about/faculty.html"},
    {"name": "University of Toronto", "url": "https://www.utoronto.ca/faculty-directory"},
    {"name": "University of Edinburgh", "url": "https://www.ed.ac.uk/contacts/faculty"},
    {"name": "Cornell University", "url": "https://www.cs.cornell.edu/people/faculty"},
    {"name": "Peking University", "url": "https://english.pku.edu.cn/faculty"},
    {"name": "UCL", "url": "https://www.ucl.ac.uk/computer-science/people"},
    {"name": "McGill University", "url": "https://www.mcgill.ca/engineering/people/faculty"},
    {"name": "UNSW Sydney", "url": "https://www.unsw.edu.au/computing/people"},
    {"name": "University of Michigan", "url": "https://www.eecs.umich.edu/people/faculty"},
    {"name": "University of Texas at Austin", "url": "https://www.cs.utexas.edu/people/faculty"},
    {"name": "NYU", "url": "https://www.nyu.edu/academics/faculty.html"},
    {"name": "Georgia Tech", "url": "https://www.cc.gatech.edu/people/faculty"},
    {"name": "University of Queensland", "url": "https://www.uq.edu.au/contacts/faculty"},
    {"name": "Monash University", "url": "https://www.monash.edu/it/people/faculty"},
    {"name": "University of Melbourne", "url": "https://www.unimelb.edu.au/faculty"},
    {"name": "University of Wisconsin-Madison", "url": "https://www.wisc.edu/directory/faculty"},
    {"name": "King's College London", "url": "https://www.kcl.ac.uk/people"},
    {"name": "University of Wollongong", "url": "https://www.uow.edu.au/contacts/faculty"},
    {"name": "University of London", "url": "https://www.london.ac.uk/about-us/people/faculty"},
    {"name": "University of Adelaide", "url": "https://www.adelaide.edu.au/contacts/faculty"},
    {"name": "University of Bristol", "url": "https://www.bristol.ac.uk/people"},
    {"name": "Duke University", "url": "https://www.duke.edu/people/faculty"},
    {"name": "ANU", "url": "https://www.anu.edu.au/directories/faculty"},
    {"name": "University of Sydney", "url": "https://www.sydney.edu.au/about-us/people/faculty"},
    {"name": "Rice University", "url": "https://cs.rice.edu/people/faculty"},
    {"name": "Penn State", "url": "https://www.psu.edu/directory/faculty"},
    {"name": "University of Pennsylvania", "url": "https://www.upenn.edu/directories/faculty"},
    {"name": "University of Warwick", "url": "https://warwick.ac.uk/faculty-directory"},
    {"name": "KU Leuven", "url": "https://www.kuleuven.be/faculty-directory"},
    {"name": "University of Hong Kong", "url": "https://www.hku.hk/people/faculty-directory"}
]

# Output CSV file
output_file = "faculty_info.csv"

# Open the CSV file for writing
with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(["Name", "Description"])

    # Iterate through each website
    for site in websites:
        try:
            response = requests.get(site["url"], timeout=10)  # Set a timeout for robustness
            soup = BeautifulSoup(response.content, "html.parser")
            
            print(f"Processing data from {site['name']} ({site['url']})...")

            # Extract all divs with their classes and text
            for div in soup.find_all("div"):
                class_name = div.get("class")  # Get class name
                text_content = div.get_text(strip=True)  # Get text content
                if class_name and text_content:  # Check if both exist
                    description = f"Class: {class_name}, Text: {text_content}"
                    # Write data to the CSV
                    writer.writerow([site["name"], description])

            print(f"Finished processing {site['name']}\n")
        except Exception as e:
            print(f"Error processing {site['url']}: {e}")

print(f"Data saved to {output_file}")
