import requests
from bs4 import BeautifulSoup
import csv

# List of university websites
websites = [
    "https://www.cs.ox.ac.uk",  # University of Oxford
    "https://www.cs.stanford.edu",  # Stanford University
    "https://www.eecs.mit.edu",  # Massachusetts Institute of Technology (MIT)
    "https://www.cam.ac.uk",  # University of Cambridge
    "https://cs.berkeley.edu",  # University of California, Berkeley
    "https://www.cmu.edu",  # Carnegie Mellon University
    "https://www.harvard.edu",  # Harvard University
    "https://www.caltech.edu",  # California Institute of Technology
    "https://www.columbia.edu",  # Columbia University
    "https://www.ucla.edu",  # University of California, Los Angeles (UCLA)
    "https://www.uw.edu",  # University of Washington
    "https://www.uchicago.edu",  # University of Chicago
    "https://www.tsinghua.edu.cn",  # Tsinghua University
    "https://www.ethz.ch",  # ETH Zurich (Swiss Federal Institute of Technology)
    "https://www.imperial.ac.uk",  # Imperial College London
    "https://www.yale.edu",  # Yale University
    "https://www.princeton.edu",  # Princeton University
    "https://www.nus.edu.sg",  # National University of Singapore (NUS)
    "https://www.tum.de",  # Technical University of Munich (TUM)
    "https://www.epfl.ch",  # École Polytechnique Fédérale de Lausanne (EPFL)
    "https://www.u-tokyo.ac.jp",  # University of Tokyo
    "https://www.utoronto.ca",  # University of Toronto
    "https://www.ed.ac.uk",  # University of Edinburgh
    "https://www.cornell.edu",  # Cornell University
    "https://www.pku.edu.cn",  # Peking University
    "https://www.ucl.ac.uk",  # University College London (UCL)
    "https://www.mcgill.ca",  # McGill University
    "https://www.unsw.edu.au",  # University of New South Wales (UNSW Sydney)
    "https://www.umich.edu",  # University of Michigan
    "https://www.utexas.edu",  # University of Texas at Austin
    "https://www.nyu.edu",  # New York University (NYU)
    "https://www.monash.edu",  # Monash University
    "https://www.washington.edu",  # University of Washington
    "https://www.unimelb.edu.au",  # University of Melbourne
    "https://www.kcl.ac.uk",  # King's College London
    "https://www.uow.edu.au",  # University of Wollongong
    "https://www.london.ac.uk",  # University of London
    "https://www.unsw.edu.au",  # University of New South Wales
    "https://www.bristol.ac.uk",  # University of Bristol
    "https://www.duke.edu",  # Duke University
    "https://www.anu.edu.au",  # Australian National University
    "https://www.sydney.edu.au",  # University of Sydney
    "https://www.rice.edu",  # Rice University
    "https://www.wisc.edu",  # University of Wisconsin-Madison
    "https://www.psu.edu",  # Pennsylvania State University
    "https://www.upenn.edu"  # University of Pennsylvania
]

# Function to get all links from a webpage
def get_links(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', href=True)
        return [link['href'] for link in links if link['href'].startswith("http") or link['href'].startswith("/")]
    except Exception as e:
        print(f"Error fetching links from {url}: {e}")
        return []

# Write the links to a CSV for manual review
with open("university_links.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["University", "Link"])
    
    for website in websites:
        print(f"Processing: {website}")
        links = get_links(website)
        for link in links:
            # Ensure the link is complete
            full_link = link if link.startswith("http") else website.rstrip("/") + link
            writer.writerow([website, full_link])

print("Links saved to 'university_links.csv'. Review the file to handpick relevant links.")
