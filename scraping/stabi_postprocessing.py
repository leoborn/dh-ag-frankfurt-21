"""
This script is used to post-process the data scraped with the script multi_page_scraping_stabi.py.

We use this to:
  * separate Japanese from Romaji names
  * normalize dates
  * analyze the contents of the "Text" field

Run this script like this: python stabi_postprocessing.py
"""
import json
# With this, we can use regular expressions.
import re
# We import this sub-class for easy generation of frequency distributions.
from nltk import FreqDist
# This library is for normalizing dates.
import dateparser
# This is the NLP toolkit we use.
import spacy
# We initialize a German NLP pipeline with the medium-sized language model.
nlp = spacy.load('de_core_news_md')

with open("japanese_students.json") as json_file:
  data = json.load(json_file)

print("Number of students:", len(data))

# Student name processing
# Task: Separate Japanese from Romaji names
#
# We define a regular expression for a sequence of unicode characters in the CJK range.
JAPANESE_CHARACTERS_PATTERN = r'[\u4e00-\u9fff]+'
for student in data:
  print(student)
  name = student['Name']
  jap_characters_found = re.findall(JAPANESE_CHARACTERS_PATTERN, name)
  print(jap_characters_found)
  # This means that no Japanese characters appear in the name.
  if len(jap_characters_found) == 0:
    print("No Japanese name!")
    print("Romaji name:", name)
  else:
    # Japanese name is the last element of the String split at whitespaces.
    name_jpn = name.split(" ")[-1]
    print("Japanese Name:", name_jpn)
    # For the Romaji name, we take all elements except the last of the String split at whitespaces.
    # For example, this might result in ["Abe", "Isoo"].
    # We then join this List to a String using a whitespace -> "Abe Isoo".
    name_romaji = " ".join(name.split(" ")[:-1])
    print("Romaji Name:", name_romaji)


# Student date processing
# Task: Separate Japanese from Romaji names
# 
# We might encounter ill-formed dates, so we set a counter to see how many dates could not be parsed.
unparseable_dates = 0
# We initialize an empty List to collect all parsed birth years.
birth_year_list = []
for student in data:
  dates = student['Daten']
  # Dates are given in the format date1–date2.
  print("Birth and death dates:", dates)
  # We separate them by splitting at "–".
  date_list = dates.strip().split("–")
  # We are only interested in dates that are not just "-".
  #
  # Examples:
  # A date "-1913" would result in ["","1913"],
  # a date "Juni 1880-" would result in ["Juni 1880",""],
  # and a date "3.4.1857-Dezember 1910" would result in ["3.4.1857", "Dezember 1910"].
  if len(date_list) == 2:
    first_date = date_list[0]
    second_date = date_list[1]
    # Only continue if non-empty.
    if first_date != "":
      try:
        birth_date = dateparser.parse(first_date)
        print("Birth date:", birth_date)
        # The year of a parsed date can be accessed with .year.
        print("Birth year:", birth_date.year)
        birth_year_list.append(birth_date.year)
      except:
        print(first_date, "cannnot be parsed!")
        unparseable_dates += 1
    # Only continue if non-empty.
    if second_date != "":
      try:
        death_date = dateparser.parse(second_date)
        print("Death date:", death_date)
        print("Death year:", death_date.year)
      except:
        print(second_date, "cannnot be parsed!")
        unparseable_dates += 1

print(unparseable_dates, "dates could not be parsed.")
# Automatically generate a frequency distribution from the birth year List.
fdist = FreqDist(birth_year_list)
# Print out the 20 most common birth years.
print("Most common birth years and their frequencies:")
print(fdist.most_common(20))


# Student text processing
# Task 1: Retrieve all visited universities and their frequencies
#
# Initialize empty list of found universities.
all_universities = []
for student in data:
  text = student['Text']
  # Running spacy on the text amounts to calling nlp(text).
  parsed_text = nlp(text)
  # We can access all named entities using .ents.
  for named_entity in parsed_text.ents:
    # We take all named entities starting with "U " (e.g. "U Berlin") to be indicative of a university.
    if named_entity.text.startswith("U "):
      all_universities.append(named_entity.text)
uni_fdist = FreqDist(all_universities)
print("Most common universities and their frequencies:")
print(uni_fdist.most_common(20))


# Task 2: Retrieve all place names from the text commentary
#
# We initialize an empty dictionary.
persons_to_text_places = {}
for student in data:
  name = student['Name']
  persons_to_text_places[name] = []
  text = student['Text']
  # Running spacy on the text amounts to calling nlp(text).
  parsed_text = nlp(text)
  # We can access all named entities using .ents.
  for named_entity in parsed_text.ents:
    if named_entity.label_ == "LOC":
      persons_to_text_places[name].append(named_entity.text)