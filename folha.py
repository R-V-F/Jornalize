import requests
from bs4 import BeautifulSoup
import mysql.connector
from datetime import datetime
import json

# Read the JSON file
with open('config.json', 'r') as file:
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


def scrape_news(url):
    # Send an HTTP request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract information based on the HTML structure of the website
        latest_articles_ol = soup.find('ol', 'u-list-unstyled')
        latest_articles_html = latest_articles_ol.find_all('li','c-headline')
        i = 0
        # Print the titles of the articles
        for latest in latest_articles_html:
            i += 1
            article_title_html = latest.find('h2')
            article_title = article_title_html.text.encode('latin-1').decode('utf-8', 'ignore')
            article_link_html = latest.find('a')
            article_link = article_link_html.get('href')
            # if(article_link in urls_list): 
            #     print('repeated result')
            #     continue
            img_src_html = latest.find('img','c-headline__image')
            if(img_src_html is not None): img_src = img_src_html.get('data-src')
            else: img_src = 'NULL'
            article_timestamp_html = latest.find('time')
            article_timestamp = article_timestamp_html.get('datetime')

            
            try:
                query = f"INSERT INTO db_projn.noticias (url,titulo, imgsrc, data, fonte) VALUES (%s, %s, %s, %s, %s);"
                cursor.execute(query, (article_link,article_title,img_src,article_timestamp, 'folha'))
                connection.commit()
                print(i)
                print(article_title)
                print(article_link)
                print(article_timestamp)
                print(img_src)
            except Exception as e:
                # Handle other exceptions
                print(f"An unexpected error occurred:{i} \n{e}")
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")

if __name__ == "__main__":
    # Replace this URL with the website you want to scrape
    economia_url = "https://www1.folha.uol.com.br/mercado/"
    politica_url = "https://www1.folha.uol.com.br/poder/"
    
    scrape_news(economia_url)
    scrape_news(politica_url)
    # Close the cursor and connection
    cursor.close()
    connection.close()