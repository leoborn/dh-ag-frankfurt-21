"""
This script downloads the HTML data from a URL and parses it using BeautifulSoup.

It demonstrates some basic functions of the BeautifulSoup library and shows how to extract information from web pages.

Run this script like this: python single_page_scraping.py
"""

# This sub-package allows us to retrieve the contents of an URL.
import urllib.request
# This sub-package is used to encode CJK/unicode characters in an URL.
import urllib.parse
# Our HTML parser is provided by BeautifulSoup.
from bs4 import BeautifulSoup

LINK_ENG = 'https://en.wikipedia.org/wiki/Japan'
LINK_JPN = 'https://ja.wikipedia.org/wiki/' + urllib.parse.quote('日本')

# Here, we create an HTTP request for the chosen URL.
page = urllib.request.Request(LINK_ENG, headers={'User-Agent': 'Mozilla/5.0'})
# These two lines now actually retrieve the contents of the URL and
# store them in the variable "html_data"
with urllib.request.urlopen(page) as response:
  html_data = response.read()

#print(html_data)

# This is the main part, allowing us to parse the HTML data retrieved above.
soup = BeautifulSoup(html_data, 'html.parser')
#print(soup.title)
#print(soup.title.string)
#print(soup.get_text())

# Example 1: Get the table of contents of the Wikipedia page.
#
# There are two approaches to this:
#
# 1.
# 1.1. Iterate over all div elements.
for div in soup.find_all('div'):
  # Get a div's ID and check if it says "toc".
  if div.get('id') == "toc":
    # If so, use it as the TOC
    toc = div
    # Break the loop as we do not need to check any more divs.
    break
#print("TOC (first method):", toc)
#
# OR
#
# 2.
# 2.1. Get the first div element with id "toc" in one command.
toc = soup.find(name="div", attrs={"id":"toc"})
#print("TOC (second method):", toc)

# We just want to show the text of the TOC, so
# we get the outermost list element
toc_list = toc.find('ul')
#print(toc_list)
# We iterate over each list element that has the class "toclevel-1".
for list_element in toc_list.find_all(name="li", attrs={"class":"toclevel-1"}):
    # We print out the text of the list element without surrounding whitespaces.
    print(list_element.text.strip())


# Example 2: Get the basic tabular data from the info box of a Wikipedia page.
#
# Initialize empty dictionary to store contents of infobox.
infobox_dict = {}
# Get the first table element with class "infobox".
infobox = soup.find(name="table", attrs={"class":"infobox"})
# Iterate over all table rows in the infobox.
for table_row in infobox.find_all('tr'):
  # Get the row's first column.
  row_key = table_row.find('th')
  # Get the row's second column.
  row_value = table_row.find('td')
  # Only proceed if both are valid
  if row_key is not None and row_value is not None:
    # Get the text values for first and second columns.
    row_key_text = row_key.text
    row_value_text = row_value.text
    print(row_key_text,":", row_value_text)
    infobox_dict[row_key_text] = row_value_text

print("Infobox:", infobox_dict)