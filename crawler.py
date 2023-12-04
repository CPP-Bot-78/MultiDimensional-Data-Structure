from operator import index
import requests
from bs4 import BeautifulSoup
import pandas as pd
import spacy
import re



# for dblp.org
scientists_names=[]
# Load the spacy model for text vectorization
nlp = spacy.load('en_core_web_sm')
# The main list of computer scientists' Wikipedia URL
main_page_url = 'https://en.wikipedia.org/wiki/List_of_computer_scientists'
dblp_url = "https://dblp.org/search?q=author%3A"


# Function to get the list of scientists' Wikipedia page URLs
def get_scientists_urls(main_page_url):
    response = requests.get(main_page_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    list_items = soup.select('.mw-parser-output > ul > li')
    base_url = 'https://en.wikipedia.org'
    scientist_urls = [base_url + item.find('a')['href'] for item in list_items if item.find('a')]
    return scientist_urls


# Function to extract data from individual Wikipedia page
def extract_data_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the name considering the presence of parenthesis
    title = soup.find('h1', {'id': 'firstHeading'}).text
    # Check if the title contains parentheses and extract accordingly
    if '(' in title:
        name = title.split('(')[0].strip().split(' ')[-1]  # Get last word before parenthesis
        firstname = title.split('(')[0].strip().split(' ')[0]
        scientists_names.append((firstname,name))
    else:
        name = title.split(' ')[-1]  # Get last word of the title if no parenthesis
        firstname = title.split('(')[0].strip().split(' ')[0]
        scientists_names.append((firstname,name))
    #scientists_names

  
    # Function to count awards in a given container
    def count_awards_in_container(container):
        # Find all 'li' tags, if any
        list_items = container.find_all('li')
        if list_items:
            return len(list_items)
        else:
            # If there are no 'li' tags, it's likely just plain text.
            # Here we count the number of awards by splitting the text at <br> tags.
            # This is a simple heuristic and might not be accurate if the format is inconsistent.
            br_tags = container.find_all('br')
            if br_tags:
                return len(br_tags) + 1
            else:
                # If there are no 'br' tags, count each non-empty line as an award
                text_awards = container.get_text(separator='\n').split('\n')
                return len([award for award in text_awards if award.strip() != ''])

    # Start by checking the infobox
    infobox = soup.find('table', {'class': 'infobox'})
    awards_count = 0
    if infobox:
        awards_row = infobox.find('th', string=re.compile('Awards', re.I))
        if awards_row:
            awards_data = awards_row.find_next_sibling('td')
            if awards_data:
                awards_count = count_awards_in_container(awards_data)

    # If no awards are found in the infobox, look in the main content
    if awards_count == 0:
        awards_section = soup.find('span', {'class': 'mw-headline'}, string=re.compile('Awards', re.I))
        if awards_section:
            # Get the container of the awards section which might be within a div or the next 'ul' or 'ol
            next_element = awards_section.find_next()
            while next_element and next_element.name not in ["ul", "ol"]:
                next_element = next_element.find_next()

            if next_element and next_element.name in ["ul", "ol"]:
                awards_count = count_awards_in_container(next_element)

    # Find the 'Alma mater' row in the infobox
    infobox = soup.find('table', {'class': 'infobox'})
    education_vector = []  # Initialize an empty list to store 'Alma mater' names
    if infobox:
        # Find 'th' elements with 'infobox-label', then iterate to match 'Alma mater' with non-breaking spaces
        for th in infobox.find_all('th', {'class': 'infobox-label'}):
            # Use .get_text() and replace to handle non-breaking spaces and compare
            if 'Alma mater' in th.get_text().replace(u'\xa0', u' '):
                # If found, get the next sibling 'td' element containing the universities
                alma_mater_data = th.find_next_sibling('td')
                if alma_mater_data:
                    # Get all anchor tags within the 'Alma mater' data cell
                    alma_mater_links = alma_mater_data.find_all('a')
                    # Extract the text from each anchor tag and add it to the education_vector list
                    education_vector = [link.get_text() for link in alma_mater_links if link.get_text().strip()]
                break  # Stop the loop after finding the 'Alma mater' row
    if not education_vector and infobox:
        for th in infobox.find_all('th', {'class': 'infobox-label'}):
            # Use .get_text() and replace to handle non-breaking spaces and compare
            if 'Education' in th.get_text().replace(u'\xa0', u' '):
                # If found, get the next sibling 'td' element containing the universities
                alma_mater_data = th.find_next_sibling('td')
                if alma_mater_data:
                    # Get all anchor tags within the 'Alma mater' data cell
                    alma_mater_links = alma_mater_data.find_all('a')
                    # Extract the text from each anchor tag and add it to the education_vector list
                    education_vector = [link.get_text() for link in alma_mater_links if link.get_text().strip()]
                break  # Stop the loop after finding the 'Alma mater' row
    if not education_vector:
        education_section = soup.find('span', {'class': 'mw-headline', 'id': 'Education'})
        if education_section:
            # Get the container of the education section which is usually a preceding sibling of h2 containing the 'Education' span
            edu_container = education_section.find_parent('h2').find_next_sibling(
                lambda tag: tag.name in ["ul", "p", "div"])
            if edu_container:
                university_links = edu_container.find_all('a', string=lambda text: 'Uni' in text if text else False)
                if university_links:
                    # Add the text of the first valid 'University' link
                    education_vector.append(university_links[0].get_text())

    if not education_vector:
        bio_section = soup.find('span', {'class': 'mw-headline', 'id': 'Biography'})
        if bio_section:
            # Get the container of the education section which is usually a preceding sibling of h2 containing the 'Education' span
            bio_container = bio_section.find_parent('h2').find_next_sibling(lambda tag: tag.name in ["ul", "p", "div"])
            if bio_container:
                university_links = bio_container.find_all('a', string=lambda text: 'Uni' in text if text else False)
                if university_links:
                    # Add the text of the first valid link containing 'Uni'
                    education_vector.append(university_links[0].get_text())

    return {
        'Surname': name,
        '#Awards': awards_count,
        'Education': education_vector  # Convert numpy array to list for easier handling
    }

def get_dblp(dbplp_url):
    response = requests.get(dbplp_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    dplp_element = soup.find(attrs={'id':'completesearch-info-matches'}).encode_contents()
    if dplp_element == "no matches":
        return 0
    else:
        dplp_num = re.sub("[^0-9]", "", f"{dplp_element}")
        return dplp_num



# Get the list of individual Wikipedia URLs for the scientists
scientists_urls = get_scientists_urls(main_page_url)

# List to hold the data
data = []

# Iterate over the URLs and extract data
for url in scientists_urls[:678]:
    try:
        scientist_data = extract_data_from_page(url)
        data.append(scientist_data)
        print(f"Data extracted for {scientist_data['Surname']}")
    except Exception as e:
        print(f"Failed to extract data for URL {url}: {e}")


dblp_url='https://dblp.org/search?q=author%3A'
dblp_list=[]
for name in scientists_names:
    if "Wikipedia" in name[0] or "Wikipedia" in name[1]:
        break
    new_url=dblp_url+ name[0] + "%20" + name[1]
    try:
        dblp=get_dblp(new_url)
        dblp_list.append((dblp,name[1]))
        print(f"DBLP data extracted for {name[1]}")
    except Exception as e:
        print(f"Failed to extract DBLP data for {name[1]}: {e}")
        dblp_list.append((0,name[1]))



# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(data)

for value in dblp_list:
    if value[1] in df['Surname'].values:
        df.loc[df['Surname'] == value[1], 'DBLP'] = value[0]
        print(f"Added {value[1]}'s DBLP match in DataFrame")

#clear values with no DBLP
df = df.dropna(axis=0,how="any")
# Fix integer types
df = df.convert_dtypes()

# Optionally, save the DataFrame to a CSV file
df.to_csv('computer_scientists_data.csv', index=True)
