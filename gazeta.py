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

# Specify the format of the input string
format_string = "%d/%m/%Y %H:%M"


# Create a cursor object to interact with the database
cursor = connection.cursor()

def getAuthor(url):
    # Send an HTTP request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        article_author_html = soup.find('a','author-name-link')
        if(article_author_html is not None): 
            article_author = article_author_html.text.strip().encode('latin-1').decode('utf-8', 'ignore')
            print(article_author)
            return article_author
        else:
            article_author_html = soup.find('span','author-name')
            if(article_author_html is not None):
                article_author = article_author_html.text.strip().encode('latin-1').decode('utf-8', 'ignore')
                print(article_author)
                return article_author
            else:
                return -1 
    else:
        print(f"Failed to fetch the page getAuthor. Status code: {response.status_code}")

def scrape_news(url):
    # Send an HTTP request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract information based on the HTML structure of the website
        articles = soup.find_all('div', 'item-list')

        i = 0
        # Print the titles of the articles
        for article in articles:
            article_link_html = article.find('a')
            article_link = 'https://www.gazetadopovo.com.br' + article_link_html.get('href')
            i += 1
            article_title_html = article.find('h2')
            article_title = article_title_html.text.encode('latin-1').decode('utf-8', 'ignore') # tira os caracteres estranhos
            article_timestamp_html = article.find('div','publish-at')
            article_timestamp = article_timestamp_html.text
            img_src_html = article.find('img')
            if(img_src_html is not None): img_src = img_src_html.get('data-src')
            else: img_src = 'NULL'
            # Convert the string to a datetime object
            datetime_object = datetime.strptime(article_timestamp, format_string)
            # Format the datetime object as a string in the desired format
            formatted_datetime = datetime_object.strftime(f"%Y-%m-%d %H:%M:%S")
            #YYYY-MM-DD HH:MM:SS
            article_author = getAuthor(article_link)
            if(article_author == -1): continue
            try:
                query = f"INSERT INTO db_projn.noticias (url,titulo, imgsrc, data, fonte, autor) VALUES (%s, %s, %s, %s, %s, %s);"
                cursor.execute(query, (article_link,article_title,img_src,formatted_datetime, 'Gazeta do Povo',article_author))
                connection.commit()
                print('count:',i)
                print(article_title)
                print(article_link)
                print(article_author)
                print(formatted_datetime)
                print(img_src)
                print(query)
            except Exception as e:
                # Handle other exceptions
                print(f"An unexpected error occurred:{i} \n{e}")
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")

if __name__ == "__main__":
    # Replace this URL with the website you want to scrape
    target_url = "https://www.gazetadopovo.com.br/ultimas-noticias/?ref=explore"
    
    # Call the function with the target URL
    scrape_news(target_url)

    # Close the cursor and connection
    cursor.close()
    connection.close()