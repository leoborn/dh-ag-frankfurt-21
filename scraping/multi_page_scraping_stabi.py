"""
This scraper iterates through the online list of Japanese students in Germany during the Meiji era and downloads information on them.

It demonstrates the usage of scrapy as part of a standard Python script.
This was done because we intend to first iterate over all pages and collect information on all persons,
and only save them once after we are done scraping the information.

Run this script like this: python multi_page_scraping_stabi.py
"""

import scrapy
# Because we want to run the scraper from within the script, we need to import CrawlerProcess.
from scrapy.crawler import CrawlerProcess
# Because we will save the data as JSON at the end.
import json

# Here, we initialize an empty list for all persons that we find.
COLLECTED_PEOPLE = []

# Our main scraper, StabiSpider. This is a self-contained class that defines what our crawler is.
class StabiSpider(scrapy.Spider):

    # The following are four class variables, associated with each instance of our StabiSpider.
    # The first two are required by scrapy.
    #
    # The crawler gets a name (required).
    name = 'stabispider'
    #
    # The list of URLs that serve as the starting point for scraping (required); we only need one.
    start_urls = ['https://themen.crossasia.org/japans-studierende/index/show']
    #
    # By inspecting the above page, we found out that each subsequent data page URL is formed like this:
    # https://themen.crossasia.org/japans-studierende/index/show/page/X
    # Our simple way of accessing every page therefore is to keep track of the current page (first variable)
    # and to access the above URL until we reach the last page (second variable). Since we do not know
    # how many pages there are in total, we set it to 0 and later get the correct value.
    current_page = 1
    last_page = 0


    # The main function of the scraper. Its first argument, self, is the StabiSpider class;
    # this allows to access the above class variables from inside the function
    # as well as to call this function, parse, from within as well.
    # The second argument, response, is what scrapy returns from fetching the web page contents.
    def parse(self, response):

        # Inspecting the page, we saw that all person data is stored as one table per person.
        # A person table looks like this (simplified):
        # <tr>
        #   <td>Name</td>
        #   <td>Arai Seishi (Seiji) 新井精司</td>
        # </tr>
        # <tr>
        #   <td>Ort</td>
        #   <td>Tôkyô</td>
        # </tr>
        # ...
        for table in response.css('table'):

            # We also saw that person table have width="100%", so we only continue if this is given.
            table_width = table.css('::attr(width)').get()
            if table_width == "100%":
                print("Person table:", table)

                # We initialize an empty person dictionary/object to store information on the person.
                new_person = {}

                # We iterate over each table row (indicated by 'tr').
                for row in table.css('tr'):
                    #print(row.css('td').getall())

                    # We now get all row data (contained in 'td').
                    row_elements = row.css('td')
                    # IMPORTANT: The reason we do not iterate over it (as with 'tr') is as follows:
                    # All rows contain two elements. But only in the "Name" row, the value element additionally contains a comment button.
                    # This makes accessing the actual name value different from accessing any other value (e.g. value for "Ort").

                    # Therefore, we first access the first element, the attribte (e.g. "Name", "Ort" ...).
                    attribute = row_elements[0].css('td ::text').get()
                    print("Attribute:", attribute)

                    # If the attribute is "Name", we get the name value using the boldface selector.
                    if attribute == "Name":
                        value = row_elements[1].css('b ::text').get()
                    # For all other attributes, we use the simpler 'td' selector.
                    else:
                        value = row_elements[1].css('td ::text').get()
                    print("Value:", value)

                    # Now, we fill the new_person object with the obtained information.
                    # For example, after retrieving the name, it looks like this:
                    # new_person == {'Name': 'Arai Seishi (Seiji) 新井精司'}
                    new_person[attribute] = value
                
                # After we are done retrieving person information from all rows, we add the complete person object
                # to our global list of collected persons.
                COLLECTED_PEOPLE.append(new_person)
        

        # After we are done with all tables on the page, we can move on to the next page,
        # provided there is one. To do this, we need information on what the last page number is.
        #
        # If we have not yet determined what the last page number is,
        # we need to identify it here once.
        if self.last_page == 0:
            # We know that pagination is inside a div with class "pages",
            # therefore we select all links under the "pages" divs.
            pagination = response.css('.pages a')
            print(pagination)

            # We know that the last page link is the last element of the list ([-1]),
            # so we only access this element and get its "href" value.
            link_to_last_page = pagination[-1].css('::attr(href)').get()
            print(link_to_last_page)
            
            # We know the link is formed "index/show/page/X" so in order to get the number,
            # we split at that substring and take the last element (X) and cast it as an integer.
            self.last_page = int(link_to_last_page.split("index/show/page/")[-1])
            print("Last page number:", self.last_page)

        # Only access the next page if the current page value is smaller than or equal to the last page value.
        if self.current_page <= self.last_page:
            # Form the URL for the next page based on the rule we figured out.
            next_page = self.start_urls[0] + '/page/' + str(self.current_page)
            print("Next page URL:", next_page)

            # Increment the current page counter so it is updated for the next page
            self.current_page += 1

            # Open the URL of the next page and use this function, parse, to extract its contents.
            request = scrapy.Request(next_page, callback=self.parse)
            yield request 


# The following is needed for running scrapy from within a script.
# We first create a process with the signature of a web browser.
process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
# Then we use this process to invoke our StabiSpider
process.crawl(StabiSpider)
# This ensures that all the subseqeunt code will only be executed once the crawling is finished.
process.start()

print("Finished scraping. We collected", len(COLLECTED_PEOPLE),"persons from the source!")
"""
with open("japanese_students.json", 'w') as result_file:
    json_string = json.dumps(COLLECTED_PEOPLE, indent=4)
    result_file.write(json_string)
"""