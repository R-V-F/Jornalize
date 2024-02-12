import requests
from bs4 import BeautifulSoup
import mysql.connector
from datetime import datetime
import json
import re
import os

directory = os.path.dirname(os.path.abspath(__file__))
file_name = 'config.json'

full_path = os.path.join(directory, file_name)

# Read the JSON file
with open(full_path, 'r') as file:
    config_data = json.load(file)
# Access the values
host = config_data['host']
user = config_data['user']
password = config_data['password']
database = config_data['database']

# Establish a connection to the MySQL server
connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

# Create a cursor object to interact with the database
cursor = connection.cursor()

# Specify the format of the input string
format_string = "%d/%m/%Y %H:%M"

def getAuthor(url):
    # Send an HTTP request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract information based on the HTML structure of the website
        article_author_html = soup.find('div', 'name')
        if(article_author_html is not None):
            author_raw = article_author_html.text.strip().encode('latin-1').decode('utf-8', 'ignore')
            author_split1 = author_raw.split('  ', 2)
            author_split2 = author_split1[0].split('\n')
            author_clean = re.sub(r'[^a-zA-Z0-9\s]', '', author_split2[0])
            return author_clean
        return ''
    else:
        print(f"Failed to fetch the get author page. Status code: {response.status_code}")
        return ''

def scrape_news(url):
    # Send an HTTP request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract information based on the HTML structure of the website
        latest_articles_ul = soup.find('ul', id='list-ultimas-editoria')
        latest_articles_li = latest_articles_ul.find_all('li')
        i = 0
        # Print the titles of the articles
        for latest in latest_articles_li:
            i += 1
            article_title_html = latest.find('h2')
            article_title = article_title_html.text.encode('latin-1').decode('utf-8', 'ignore')
            article_link_html = latest.find('a')
            article_link = 'https://www.correiobraziliense.com.br' + article_link_html.get('href')
            article_timestamp_html = latest.find('small')
            article_timestamp = article_timestamp_html.text[11:]
            # Convert the string to a datetime object
            datetime_object = datetime.strptime(article_timestamp, format_string)
            # Format the datetime object as a string in the desired format
            formatted_datetime = datetime_object.strftime(f"%Y-%m-%d %H:%M:%S")
            # Get img src
            img_src_html = latest.find('img')
            if(img_src_html is not None): img_src = img_src_html.get('data-src')
            else: img_src = 'NULL'
            author = getAuthor(article_link)
            print(author)
            print(article_link)
            print(i)
            try:
                query = f"INSERT INTO db_projn.noticias (url,titulo, imgsrc, data, fonte, autor) VALUES (%s, %s, %s, %s, %s, %s);"
                cursor.execute(query, (article_link,article_title,img_src,formatted_datetime, 'Correio Braziliense', author))
                connection.commit()
                print(i)
                print(article_title)
                print(article_link)
                print(formatted_datetime)
                print(img_src)
                print(author)
                print(query)
            except Exception as e:
                # Handle other exceptions
                print(f"An unexpected error occurred:{i} \n{e}")
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")

if __name__ == "__main__":
    # Replace this URL with the website you want to scrape
    economia_url = "https://www.correiobraziliense.com.br/economia"
    politica_url = "https://www.correiobraziliense.com.br/politica"
    
    scrape_news(economia_url)
    scrape_news(politica_url)

    
    # Close the cursor and connection
    cursor.close()
    connection.close()