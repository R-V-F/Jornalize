import requests
from bs4 import BeautifulSoup
import mysql.connector
from datetime import datetime
import json
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

def getAuthor(url):
     # Send an HTTP request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        article_author_html = soup.find('strong','c-signature__author')
        if(article_author_html is not None):
            article_author = article_author_html.text.strip().encode('latin-1').decode('utf-8', 'ignore')
            return article_author
        else:
            article_author_html = soup.find('h4','c-top-columnist__name')
            if(article_author_html is not None):
                article_author = article_author_html.text.strip().encode('latin-1').decode('utf-8', 'ignore')
                return article_author
            else:
                return ''
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")

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
            article_author = getAuthor(article_link)            
            try:
                query = f"INSERT INTO db_projn.noticias (url,titulo, imgsrc, data, fonte, autor) VALUES (%s, %s, %s, %s, %s, %s);"
                cursor.execute(query, (article_link,article_title,img_src,article_timestamp, 'Folha de S. Paulo',article_author))
                connection.commit()
                # print(i)
                # print(article_title)
                # print(article_link)
                # print(article_author)
                # print(article_timestamp)
                # print(img_src)
            except Exception as e:
                # Handle other exceptions
                if('Duplicate' not in str(e)): print(f"An unexpected error occurred:{i} \n{e}")
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")

def scrape_colunas(url):
     # Send an HTTP request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        print('caralho')
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        colunas_proxy_html = soup.find("div", id="ultimas")
        test = soup.find('block')
        colunas_html = soup.findAll("li")
        print(test)
        for coluna in colunas_html:
            coluna_title_html = coluna.find('h2','c-headline__title')
            if(coluna_title_html is not None): 
                coluna_title = coluna_title_html.text.strip()
            else:
                continue
            coluna_link_html = coluna.find('a','u-link-clean')
            if(coluna_link_html is not None):
                coluna_link = coluna_link_html.get('href')
            else:
                continue
            coluna_author_html - coluna.find('h3','c-author__kicker')
            if(coluna_author_html is not None): 
                coluna_author = coluna_author_html.text.strip()
            else:
                coluna_author = ''
            coluna_imgsrc_html = coluna.find('img')
            if(coluna_imgsrc_html is not None):
                coluna_imgsrc = coluna_imgsrc_html.get('src')
            else:
                coluna_imgsrc = ''
            coluna_timestamp_html = coluna.find('time')
            if(coluna_timestamp_html is not None):
                coluna_timestamp = coluna_timestamp_html.get('datetime')
            else:
                continue
            print(coluna_title+'\n',coluna_link+'\n',coluna_author+'\n',coluna_imgsrc+'\n',coluna_timestamp+'\n')
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
if __name__ == "__main__":
    # Get the current timestamp
    current_timestamp = datetime.now()

    # Print the timestamp in a custom format
    formatted_timestamp = current_timestamp.strftime("%Y-%m-%d %H:%M:%S")
    print("Executando:", formatted_timestamp)

    with open('Colunas e Blogs _ Folha.html', 'r', encoding='utf-8') as file:
        # Read the content of the file
        html_content = file.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')

    authors_html = soup.findAll('h3','c-author__kicker')
    i = 0
    for html in authors_html:
        authors_a_html = html.find('a')
        authors_link = authors_a_html.get('href')
        if ('blog' not in authors_link) and ('f5' not in authors_link):
            i += 1
            print(authors_link, i) 

    # scrape_colunas('https://www1.folha.uol.com.br/colunaseblogs/')

    # # Replace this URL with the website you want to scrape
    # economia_url = "https://www1.folha.uol.com.br/mercado/"
    # politica_url = "https://www1.folha.uol.com.br/poder/"
    
    # scrape_news(economia_url)
    # scrape_news(politica_url)
    # # Close the cursor and connection

    # Get the current timestamp
    end_timestamp = datetime.now()

    # Print the timestamp in a custom format
    end_formatted_timestamp = end_timestamp.strftime("%Y-%m-%d %H:%M:%S")
    print("Fim:", end_formatted_timestamp)

    cursor.close()
    connection.close()
