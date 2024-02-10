import requests
from bs4 import BeautifulSoup
import mysql.connector
from datetime import datetime
import json

# Specify the format of the input string
format_string = "%d/%m/%Y %H:%M"

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

def scrape_time(url):
    # Send an HTTP request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        article_timestamp_html = soup.find('time')
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
        articles = soup.find_all('article', "cardHor")

        i = 0
        # Print the titles of the articles
        for title in articles:
            i += 1
            article_title_html = title.find('h2')
            article_title = article_title_html.text.encode('latin-1').decode('utf-8', 'ignore')
            article_link_html = title.find('a')
            article_link = article_link_html.get('href')
            img_src_html = title.find('img')
            if(img_src_html is not None): img_src = img_src_html.get('data-src')
            else: img_src = 'NULL'
            # print(i)
            # print(article_title)
            # print(article_link)
            article_timestamp = scrape_time(article_link)
            if(article_timestamp == -1): 
                print('Falha em pegar timestamp -> pulando iteracao')
                continue
            # Convert the string to a datetime object
            datetime_object = datetime.strptime(article_timestamp, format_string)
            # Format the datetime object as a string in the desired format
            formatted_datetime = datetime_object.strftime(f"%Y-%m-%d %H:%M:%S")
            #YYYY-MM-DD HH:MM:SS
            try:
                query = f"INSERT INTO db_projn.noticias (url,titulo, imgsrc, data, fonte) VALUES (%s, %s, %s, %s, %s);"
                cursor.execute(query, (article_link,article_title,img_src,formatted_datetime, 'diario do poder'))
                connection.commit()
                print(i)
                print(article_title)
                print(article_link)
                print(formatted_datetime)
                print(img_src)
            except Exception as e:
                # Handle other exceptions
                print(f"An unexpected error occurred:{i} \n{e}")
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")

if __name__ == "__main__":
    # Replace this URL with the website you want to scrape
    target_url = "https://diariodopoder.com.br/politica"
    
    # Call the function with the target URL
    scrape_news(target_url)
    
    # Close the cursor and connection
    cursor.close()
    connection.close()