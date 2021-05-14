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
import re

# Here, we initialize an empty list for all persons that we find.
COLLECTED_PEOPLE = []

# Our main scraper, StabiSpider. This is a self-contained class that defines what our crawler is.
class StabiSpider(scrapy.Spider):

    # The following are four class variables, associated with each instance of our StabiSpider.
    # The first two are required by scrapy.

    # The crawler needs a name (required)
    name = 'stabispider'
    # The list of URLs that serve as the starting point for scrapint (required)
    start_urls = ['https://themen.crossasia.org/japans-studierende/index/show']
    current_page = 1
    last_page = 0

    def parse(self, response):
        NAME_PATTERN = r'\(.*?\)'
        print("Current page:", self.current_page)
        for table in response.css('table'):
            table_width = table.css('::attr(width)').get()
            if table_width == "100%":
                print("Person table:", table)
                #print(table.css('tr').getall())
                new_person = {}
                table_rows = table.css('tr')
                for row in table_rows:
                    #print("Row:", row.get())
                    print(row.css('td').getall())
                    row_elements = row.css('td')
                    attribute = row_elements[0].css('td ::text').get()
                    print("Attribute:", attribute)
                    if attribute == "Name":
                        name = row_elements[1].css('b ::text').get()
                        print(name)
                        name = re.sub(NAME_PATTERN, '', name)
                        print(name)
                        name_jpn = name.split(" ")[-1]
                        print("Japanese Name:", name_jpn)
                        name_romaji = " ".join(name.split(" ")[:-1])
                        print("Romaji Name:", name_romaji)

                        new_person["name_jpn"] = name_jpn
                        new_person["name_romaji"] = name_romaji
                    else:
                        value = row_elements[1].css('td ::text').get()
                        print("Value:", value)
                        new_person[attribute] = value
                COLLECTED_PEOPLE.append(new_person)
        
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
            print(self.last_page)

        # Only access the next page if the current page value is smaller than or equal to the last page value.
        if self.current_page <= self.last_page:
            next_page = self.start_urls[0] + '/page/' + str(self.current_page)
            print("Next page:", next_page)
            self.current_page += 1
            request = scrapy.Request(next_page, callback=self.parse)
            yield request 

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(StabiSpider)
process.start() # the script will block here until the crawling is finished

print("Finished scraping. We collected", len(COLLECTED_PEOPLE),"persons from the source!")
#print(COLLECTED_PEOPLE)