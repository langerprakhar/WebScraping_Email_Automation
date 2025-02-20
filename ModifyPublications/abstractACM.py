import requests
from bs4 import BeautifulSoup

def get_acm_abstract(url):
    """
    Scrapes the abstract from an ACM Digital Library page using the section with id 'abstract'.

    Args:
        url (str): The URL of the ACM publication page.

    Returns:
        str: The abstract text if found, otherwise an appropriate message.
    """
    try:
        # Send a GET request to the webpage
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Look for the abstract in the section with id 'abstract'
        abstract_section = soup.find('section', id='abstract')
        if abstract_section:
            # Extract the text content and stop at 'Copy to Clipboard'
            abstract_text = abstract_section.get_text(strip=True)
            return abstract_text.split('title')[0].strip()

        return "Abstract not found on this page."

    except requests.RequestException as e:
        return f"Request error: {e}"
    except Exception as e:
        return f"An error occurred: {e}"

def get_generic_abstract(url):
    """
    Scrapes the abstract from a generic publication page by searching for the first occurrence of 'Abstract'.

    Args:
        url (str): The URL of the publication page.

    Returns:
        str: The abstract text if found, otherwise an appropriate message.
    """
    try:
        # Send a GET request to the webpage
        response = requests.get(url)
        response.raise_for_status()  # Check for successful request

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Search for the first occurrence of 'Abstract' in the page's text (case insensitive)
        tag = soup.find(text=lambda text: text and "abstract" in text.lower())
        if tag:
            # Find the parent tag that holds the abstract content (common tag is 'div', 'p', 'section', or 'article')
            abstract_section = tag.find_parent(["div", "p", "section", "article"])
            if abstract_section:
                # Extract the content from the parent tag and stop at 'Copy to Clipboard'
                abstract_text = abstract_section.get_text(strip=True)
                return abstract_text.split('title')[0].strip()

        return "Abstract not found on this page."

    except requests.RequestException as e:
        return f"Request error: {e}"
    except Exception as e:
        return f"An error occurred: {e}"

def get_abstract_from_webpage(url):
    """
    Determines the source of the URL and scrapes the abstract accordingly.

    Args:
        url (str): The URL of the publication page.

    Returns:
        str: The abstract text if found, otherwise an appropriate message.
    """
    if "dl.acm.org" in url:
        return get_acm_abstract(url)
    else:
        return get_generic_abstract(url)

# Example usage
if __name__ == "__main__":
    urls = [
        "https://proceedings.mlr.press/v70/finn17a.html",
        "http://openaccess.thecvf.com/content/CVPR2022/html/Jain_Zero-Shot_Text-Guided_Object_Generation_With_Dream_Fields_CVPR_2022_paper.html",
        "https://par.nsf.gov/biblio/10549169"
    ]
    
    for url in urls:
        print(f"URL: {url}")
        abstract = get_abstract_from_webpage(url)
        print("Abstract:", abstract)
        print()
