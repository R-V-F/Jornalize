import requests
from bs4 import BeautifulSoup
import mysql.connector
from datetime import datetime
import json
import os

directory = os.path.dirname(os.path.abspath(__file__))
file_name = 'config.json'

file_colunistas = 'lista_colunistas_folha.txt'
colunistas_path = os.path.join(directory,file_colunistas)

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
# Dont waste time on duplicates!
urls_query = f"SELECT url FROM db_projn.noticias WHERE fonte LIKE '%Folha%';"
urls_list = []
cursor.execute(urls_query)
rows = cursor.fetchall()
for row in rows:
    urls_list.append(row[0])

def scrape_colunista(url):
    response = requests.get(url)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        stop_flag = False
        ## COLUNISTA
        colunista_nome_html = soup.find('h4','c-top-columnist__name')
        if(colunista_nome_html is not None):
            colunista_nome = colunista_nome_html.text.strip().encode('latin-1').decode('utf-8', 'ignore')
            # print(colunista_nome)
        else:
            return
        ## BLOCK 1 - HEADLINE
        coluna_headline_html = soup.find('h2','c-headline__title')
        if(coluna_headline_html is not None):
            coluna_headline = coluna_headline_html.text.strip().encode('latin-1').decode('utf-8', 'ignore')
            # print(coluna_headline)
        else:
            stop_flag = True
        coluna_headline_link_html = soup.find('a','c-headline__url')
        if(coluna_headline_link_html is not None):
            coluna_headline_link = coluna_headline_link_html.get('href')
            # print(coluna_headline_link)
        else:
            stop_flag = True
        coluna_headline_timestamp_html = soup.find('time','c-headline__dateline')
        if(coluna_headline_timestamp_html is not None):
            coluna_headline_timestamp = coluna_headline_timestamp_html.get('datetime')
            # print(coluna_headline_timestamp)
        else:
            stop_flag = True
        if (stop_flag is True): 
            print('Erro com a flag.')
            return
        try:
            query = f"INSERT INTO db_projn.noticias (url,titulo, imgsrc, data, fonte, autor) VALUES (%s, %s, %s, %s, %s, %s);"
            cursor.execute(query, (coluna_headline_link,coluna_headline,'',coluna_headline_timestamp, 'Folha de S. Paulo',colunista_nome))
            connection.commit()
        except Exception as e:
            # Handle other exceptions
            if('Duplicate' not in str(e)): print(f"An unexpected error occurred:\n{e}")

        ## BLOCK 2 - LIST
        html = soup.find('ol', 'u-list-unstyled')
        coluna_list_html = html.findAll('li')
        for coluna in coluna_list_html:
            coluna_title_html = coluna.find('h2','c-headline__title')
            if(coluna_title_html is not None):
                coluna_title = coluna_title_html.text.strip().encode('latin-1').decode('utf-8', 'ignore')
                # print(coluna_title)
            else:
                continue
            coluna_link_html = coluna.find('a','c-headline__url')
            if(coluna_link_html is not None):
                coluna_link = coluna_link_html.get('href')
                if(coluna_link in urls_list): continue
                # print(coluna_link)
            else:
                continue
            coluna_timestamp_html = coluna.find('time','c-headline__dateline')
            if(coluna_timestamp_html is not None):
                coluna_timestamp = coluna_timestamp_html.get('datetime')
                # print(coluna_timestamp)
            else:
                continue
            try:
                query = f"INSERT INTO db_projn.noticias (url,titulo, imgsrc, data, fonte, autor) VALUES (%s, %s, %s, %s, %s, %s);"
                cursor.execute(query, (coluna_link,coluna_title,'',coluna_timestamp, 'Folha de S. Paulo',colunista_nome))
                connection.commit()
            except Exception as e:
                # Handle other exceptions
                if('Duplicate' not in str(e)): print(f"An unexpected error occurred:\n{e}")
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")



if __name__ == "__main__":
    # Get the current timestamp
    current_timestamp = datetime.now()

    # Print the timestamp in a custom format
    formatted_timestamp = current_timestamp.strftime("%Y-%m-%d %H:%M:%S")
    print("Executando:", formatted_timestamp)

    with open(colunistas_path, 'r') as file:
        lista_link_colunistas = file.read().splitlines()

    for url in lista_link_colunistas:
        scrape_colunista(url)
    #################### EXECUTE ESSA PARTE PARA ATUALIZAR LISTA DE COLUNISTAS
    #################### FAZER DOWNLOAD DESSA PAGINA https://www1.folha.uol.com.br/colunaseblogs/#colunas-e-blogs
    # # with open('Colunas e Blogs _ Folha.html', 'r', encoding='utf-8') as file:
    # #     # Read the content of the file
    # #     html_content = file.read()
    
    # # soup = BeautifulSoup(html_content, 'html.parser')

    # # authors_html = soup.findAll('div','c-author--blog-column')
    # # i = 0
    # # for html in authors_html:
    # #     authors_a_html = html.find('a')
    # #     author_link = authors_a_html.get('href')
    # #     author_photo_html = html.find('img')
    # #     if (author_photo_html is not None): 
    # #         author_photo = author_photo_html.get('data-src')
    # #     else:
    # #         author_photo = 'pinto'
    # #     if ('blog' not in author_link) and ('f5' not in author_link):
    # #         i += 1
    # #         print(author_link)

    # scrape_colunas('https://www1.folha.uol.com.br/colunaseblogs/') # ESSA ABORDAGEM N FUNCIONA PQ USA JS

    # Get the current timestamp
    end_timestamp = datetime.now()

    # Print the timestamp in a custom format
    end_formatted_timestamp = end_timestamp.strftime("%Y-%m-%d %H:%M:%S")
    print("Fim:", end_formatted_timestamp)

    cursor.close()
    connection.close()
