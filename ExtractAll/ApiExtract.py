import requests
from bs4 import BeautifulSoup

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
    "https://www.georgiatech.edu",  # Georgia Institute of Technology
    "https://www.uq.edu.au",  # University of Queensland
    "https://www.monash.edu",  # Monash University
    "https://www.melbourne.edu.au",  # University of Melbourne
    "https://www.washington.edu",  # University of Washington
    "https://www.unimelb.edu.au",  # University of Melbourne
    "https://www.kcl.ac.uk",  # King's College London
    "https://www.uow.edu.au",  # University of Wollongong
    "https://www.london.ac.uk",  # University of London
    "https://www.adelaide.edu.au",  # University of Adelaide
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

# Keywords to search for APIs
api_keywords = ["api", "faculty", "professors", "directory", "endpoint"]

# Function to check robots.txt for APIs
def check_robots_txt(base_url):
    try:
        robots_url = f"{base_url}/robots.txt"
        response = requests.get(robots_url, timeout=10)
        if response.status_code == 200:
            print(f"Checking {robots_url}")
            return [line for line in response.text.splitlines() if any(keyword in line for keyword in api_keywords)]
    except Exception as e:
        print(f"Error accessing {base_url}: {e}")
    return []

# Function to scrape potential API links from main pages
def find_api_links(base_url):
    try:
        response = requests.get(base_url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a', href=True)
        return [
            link['href'] for link in links
            if any(keyword in link['href'].lower() for keyword in api_keywords)
        ]
    except Exception as e:
        print(f"Error scraping {base_url}: {e}")
    return []

# Main logic to check each website
for website in websites:
    print(f"\nChecking APIs for {website}...")
    
    # Check robots.txt
    robots_results = check_robots_txt(website)
    if robots_results:
        print("Potential API endpoints in robots.txt:")
        for line in robots_results:
            print(line)
    
    # Search for links mentioning APIs
    api_links = find_api_links(website)
    if api_links:
        print("Potential API links found on the website:")
        for link in api_links:
            print(link)

    if not robots_results and not api_links:
        print("No API-related information found.")

