import requests
from bs4 import BeautifulSoup
import time
import sys

visited = []  # List of visited urls
titles = []  # List of titles of visited topics - redundant yet url comparisons was problematic -
domain = "https://wikipedia.org"
url = sys.argv[1]  # Input
title = ""  # Current visited topic title
THRESHOLD = 2  # Threshold of times to loop around same topics, after which an infinite loop is declared
TARGET_TITLE = "Philosophy"


# Loops on the root element which is passed as an argument, looks for paragraphs then hyperlinks that are children
# of these paragraphs, with some exceptions, as per Wikipedia tags, I noticed they have <a> tags that lead to localized
# directory, that being said, a manual filter had to be built using the long if condition at the center of the loop
def loop(elem):
    while elem is not None:
        parent = elem.find_next('p', class_=None)
        child = parent.find_next('a', href=True, class_=None)
        while parent is not None:
            if not child.get('href').startswith('#') and not child.get('title').startswith('Help') and not child.get(
                    'title').startswith('File'):
                print(domain + child.get('href'))
                return child.get('href')
            else:
                child = child.find_next('a', href=True, class_=None)
    return None


while True:
    r = requests.get(url)  # Requesting the HTML document
    visited.append(r.url)  # Save the current url as visited
    soup = BeautifulSoup(r.content, "html.parser")  # BeautifulSoup powerful html parsing API
    title = soup.select_one("#firstHeading").get_text()
    titles.append(title)
    if title == TARGET_TITLE:  # First break condition, if Philosophy is already reached
        print("Reached Philosophy!")
        break
    if titles.count(title) >= THRESHOLD:  # Infinite loop detector
        print("Infinite Loop Detected!")
        break
    # After doing a little bit of inspection the following id was found to encapsulate the main body paragraphs
    # Intuitively it is going to be our root tag, we will start searching for hyper links from there.
    root = soup.select_one('#mw-content-text')
    # loop function is documented above
    href = loop(root)
    if href is None:  # In case no hyper links were found
        print("No hyperlinks found in the current article!")
        break
    url = domain + href  # Retrieved hyper links lack the domain part, we are fixing that here
    time.sleep(0.5)
