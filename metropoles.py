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

def getAuthor(url):
     # Send an HTTP request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        article_author_html = soup.find('a', rel='author')
        if(article_author_html is not None): 
            article_author = article_author_html.text.strip()
            return article_author
        return -1
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        return -1

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

def scrape_news_std_model(soup):
    sucesso_head_news = 0
    try:
        # Get header news
        article_head_news_html = soup.find('div','hXCOpE')
        article_title_html = article_head_news_html.find('h2','okJeF')
        if(article_title_html is not None): article_title = article_title_html.text.strip()
        else: 
            raise Exception("Erro ao extrair titulo do artigo.")
        article_link_html = article_title_html.find('a')
        if(article_link_html is not None): article_link = article_link_html.get('href')
        else:
            raise Exception("Erro ao extrair link do artigo.")
        img_src_html = article_head_news_html.find('img','bloco-noticia__figure-imagem')
        if(img_src_html is not None): img_src = img_src_html.get('src')
        else: img_src = 'NULL'
        article_timestamp = scrape_time(article_link)
        article_fonte = 'Metrópoles'
        article_author = getAuthor(article_link)
        sucesso_head_news = 1
    except Exception as e:
        print(f"Exceção capturada: {e}")
    if(sucesso_head_news):
        try:
            query = f"INSERT INTO db_projn.noticias (url,titulo, imgsrc, data, fonte, autor) VALUES (%s, %s, %s, %s, %s, %s);"
            cursor.execute(query, (article_link,article_title,img_src,article_timestamp, article_fonte, article_author))
            connection.commit()
            print(article_title)
            print(article_link)
            print(article_timestamp)
            print(img_src)
            print(article_author)
            print(article_fonte)
            # print(query)
        except Exception as e:
            # Handle other exceptions
            print(f"An unexpected error occurred:{e}")


    try:
        # Get header news
        article_body_news_list_html = soup.findAll('div','dPsitG')
        i = 0
        for article_body_news_html in article_body_news_list_html:
            i += 1
            article_title_html = article_body_news_html.find('h4','noticia__titulo')
            if(article_title_html is not None): article_title = article_title_html.text.strip()
            else: 
                raise Exception("Erro ao extrair titulo do artigo.")
            article_link_html = article_body_news_html.find('a')
            if(article_link_html is not None): article_link = article_link_html.get('href') ### WHY IS THIS NOT WORKINGGGG
            else:
                raise Exception("Erro ao extrair link do artigo.")
            img_src_html = article_link_html.find('img','bloco-noticia__figure-imagem')
            img_src = img_src_html.get('src')
            data = scrape_time(article_link)
            article_fonte = 'Metrópoles'
            article_author = getAuthor(article_link)
            try:
                query = f"INSERT INTO db_projn.noticias (url,titulo, imgsrc, data, fonte, autor) VALUES (%s, %s, %s, %s, %s, %s);"
                cursor.execute(query, (article_link,article_title,img_src,article_timestamp, article_fonte, article_author))
                connection.commit()
                print(i)
                print(article_title)
                print(article_link)
                print(article_author)
                print(article_fonte)
                print(article_timestamp)
                print(img_src)
                print(query)
            except Exception as e:
                # Handle other exceptions
                print(f"Exceção capturada tentando escrever dados no bd:{i} \n{e}")
    except Exception as e:
        print(f"Exceção capturada tentando extrair dados: {e}")

def scrape_news_noblat_model(soup):
    articles_title_url_html = soup.findAll('div','eQcUKR') ## titulo e url
    article_timestamp_author_html = soup.findAll('div','bRvgKO') ## timestamp e autor
    article_img_src_html = soup.findAll('div','epKkgK')
    num_articles = len(articles_title_url_html)
    for i in range(0, num_articles):  # This will iterate from 0 to i-1
        try:
            article_title_html = articles_title_url_html[i].find('h2')
            if(article_title_html is not None): 
                article_title = article_title_html.text.strip()
                print('titulo',article_title)
            else: 
                raise Exception("Erro ao extrair titulo do artigo.")
            article_link_html = articles_title_url_html[i].find('a')
            if(article_link_html is not None): 
                article_link = article_link_html.get('href')
                print('link',article_link)
            else: 
                raise Exception("Erro ao extrair link do artigo.")
            article_author_html = article_timestamp_author_html[i].find('p')
            if(article_author_html is not None): 
                article_author = article_author_html.text.strip()
                print('autor',article_author)
            else:
                article_author = '' # não precisa throlar se nao achar o autor, nao é critico
            article_timestamp_html = article_timestamp_author_html[i].find('time')
            if(article_timestamp_html is not None):
                article_timestamp = article_timestamp_html.text.strip()
                article_timestamp = article_timestamp.replace('/', '-')
                print('tstamp',article_timestamp)
            else: 
                raise Exception("Erro ao timestamp link do artigo.")
            # article_img_src_html = article_img_src_html[i].find('img')
            # if(article_img_src_html is not None): 
            #     article_img_src = article_img_src_html.get('src')
            #     print('LAST img_src',article_img_src)
            # else: 
            #     article_img_src = ''
            article_img_src = ''
            article_fonte = 'Metrópoles'
            try:
                query = f"INSERT INTO db_projn.noticias (url,titulo, imgsrc, data, fonte, autor) VALUES (%s, %s, %s, %s, %s, %s);"
                print(query)                
                cursor.execute(query, (article_link,article_title,article_img_src,article_timestamp, article_fonte, article_author))
                connection.commit()
            except Exception as e:
                # Handle other exceptions
                print(f"An unexpected error occurred:{e}")
        except Exception as e:
            print(f"Exceção capturada: {e}")
    # print(i,j,k)


def scrape_news(url):
    # Send an HTTP request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        if('noblat' not in url): scrape_news_std_model(soup)
        else: scrape_news_noblat_model(soup)

    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")

if __name__ == "__main__":
    blog_noblat_link = 'https://www.metropoles.com/blog-do-noblat' #caso especial
    list_of_pages_to_track = [
    'https://www.metropoles.com/colunas/grande-angular',
    'https://www.metropoles.com/colunas/guilherme-amado',
    'https://www.metropoles.com/distrito-federal/na-mira',
    'https://www.metropoles.com/colunas/igor-gadelha',
    'https://www.metropoles.com/colunas/rodrigo-rangel',
    'https://www.metropoles.com/colunas/mario-sabino',
    'https://www.metropoles.com/colunas/paulo-cappelli',
    'https://www.metropoles.com/brasil',
    'https://www.metropoles.com/distrito-federal',
    'https://www.metropoles.com/sao-paulo',
    'https://www.metropoles.com/blog-do-noblat' #caso especial
    ]
    # for target_url in list_of_pages_to_track:
    #     # Call the function with the target URL
    #     scrape_news(target_url)
    scrape_news('https://www.metropoles.com/blog-do-noblat')
    # Close the cursor and connection
    cursor.close()
    connection.close()