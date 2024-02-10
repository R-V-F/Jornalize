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

# Specify the format of the input string
format_string = "%d/%m/%Y %H:%M"

# Establish a connection to the MySQL server
connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

# Create a cursor object to interact with the database
cursor = connection.cursor()

def scrape_time(url):
    # Send an HTTP request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        article_timestamp_html = soup.find('time', 'HeaderNoticiaWrapper__DataPublicacao-sc-4exe2y-3')
        article_timestamp = article_timestamp_html.get('datetime')
        return article_timestamp
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        return -1


def scrape_news(url):
    # Send an HTTP request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract information based on the HTML structure of the website
        article_titles = soup.find_all('div', 'jTNfwA')

        i = 0
        # Print the titles of the articles
        for title in article_titles:
            i += 1
            article_title_html = title.find('a')
            if(article_title_html is None): continue
            article_title = article_title_html.get('title').encode('latin-1', 'ignore').decode('utf-8', 'ignore')
            article_link = article_title_html.get('href')

            img_src_html = title.find('img')
            if(img_src_html is not None): img_src = img_src_html.get('src')
            else: img_src = 'NULL'

            article_timestamp = scrape_time(article_link)
            if(article_timestamp == -1): 
                print('failed to get timestamp')
                continue
            else:
                try:
                    query = f"INSERT INTO db_projn.noticias (url,titulo, imgsrc, data, fonte) VALUES (%s, %s, %s, %s, %s);"
                    cursor.execute(query, (article_link,article_title,img_src,article_timestamp, 'metropoles'))
                    connection.commit()
                    print(i)
                    print(article_title)
                    print(article_link)
                    print(article_timestamp)
                    print(img_src)
                    print(query)
                except Exception as e:
                    # Handle other exceptions
                    print(f"An unexpected error occurred:{i} \n{e}")
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")

if __name__ == "__main__":
    # Replace this URL with the website you want to scrape
    target_url = "https://www.metropoles.com/ultimas-noticias"
    
    # Call the function with the target URL
    scrape_news(target_url)
    # Close the cursor and connection
    cursor.close()
    connection.close()