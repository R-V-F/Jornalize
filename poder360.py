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


month_abbreviations = {
    'jan': '01', 'fev': '02', 'mar': '03', 'abr': '04',
    'mai': '05', 'jun': '06', 'jul': '07', 'ago': '08',
    'set': '09', 'out': '10', 'nov': '11', 'dez': '12'
}

# Establish a connection to the MySQL server
connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

# Create a cursor object to interact with the database
cursor = connection.cursor()

urls_query = f"SELECT url FROM db_projn.noticias WHERE fonte = 'poder360';"

def getAuthor(url):
    # Send an HTTP request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        article_author_html = soup.find('a', 'author')
        if(article_author_html is not None): 
            article_author = article_author_html.text.strip()
            return article_author
        return ''
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        return ''


def scrape_time(url):
    # Send an HTTP request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        article_timestamp_html = soup.find('time', 'inner-page-section__date')
        if(article_timestamp_html is not None): article_timestamp = article_timestamp_html.text
        else:
            print(f"Failed to fetch timestamp inside scrape_time function")
            result = {
                'time': -1,
                'src': 'NULL'
            }
            return result
        img_src_html2 = soup.find('div','box-skeleton--image-single')
        img_src_html = img_src_html2.find('img')
        if(img_src_html is not None): img_src = img_src_html.get('src')
        else: img_src = 'NULL'
        result = {
            'time': article_timestamp,
            'src': img_src
        }
        return result
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        result = {
            'time': -1,
            'src': 'NULL'
        }
        return result




def scrape_news(url):
    # Send an HTTP request to the URL
    response = requests.get(url)
    # Pular substring opinião
    tag_opiniao = "box-queue__special-tag"

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')


        urls_list = []
        cursor.execute(urls_query)
        rows = cursor.fetchall()
        for row in rows:
            urls_list.append(row[0])

        # Extract information based on the HTML structure of the website
        article_titles = soup.find_all('h2', 'archive-list__title-2')

        i = 0
        # Print the titles of the articles
        for title in article_titles:
            i += 1
            article_title_html = title.find('a')
            article_title = article_title_html.text
            article_link = article_title_html.get('href')
            if(article_link in urls_list or 'author' in article_link): continue
            article_author = getAuthor(article_link)
            article_timestamp = scrape_time(article_link)
            if(article_timestamp['time'] == -1): 
                print(f'\n\nFailed to get timestamp, skipping this iteration\n{article_link}\n\n')
                continue
            img_src = article_timestamp['src']
            try: # try formatting
                # Extract the date and time parts
                if('atualizado' in article_timestamp['time']):
                    new_tstamp = article_timestamp['time'].split('atualizado: ')
                    date_part, time_part = new_tstamp[1].split(' - ')
                    date_part = date_part.strip()
                    time_part = time_part.strip()
                else:
                    date_part, time_part = article_timestamp['time'].split(' - ')
                    date_part = date_part.strip()
                    time_part = time_part.strip()
            except ValueError as ve:
                print(f"\n\n\nERRO 1:\ndatepart:{date_part}\ntimepart:{time_part}\nfullstr:{article_timestamp['time']}\n{ve}\n\n\n")
                thing = article_timestamp['time'].split('-')
                print(thing)
            # Map Portuguese month abbreviations to numbers
            for month_abbrev, month_number in month_abbreviations.items():
                date_part = date_part.replace(month_abbrev + '.', month_number + '.')
            try:
                if(' ' in date_part):
                    date_part, discard = date_part.split(' ')
                    if(',' in date_part):
                        date_part, discard = date_part.split(',')
                        print(f'hey:{date_part}')
                        if(',' in date_part):
                            date_part, discard = date_part.split(',')
                elif(',' in date_part):
                    date_part, discard = date_part.split(',')
                    print(f'hey:{date_part}')
                    if(',' in date_part):
                        date_part, discard = date_part.split(',')
            except ValueError as ve:
                print(f"\n\n\nERRO 2:\ndatepart:{date_part}\ntimepart:{time_part}\nfullstr:{article_timestamp['time']}\n{ve}\n\n\n")


            # Format the date string
            formatted_date = datetime.strptime(date_part, '%d.%m.%Y').strftime('%Y-%m-%d')

            # Format the time string
            formatted_time = datetime.strptime(time_part, '%Hh%M').strftime('%H:%M')

            # Combine the date and time parts
            result_string = formatted_date + ' ' + formatted_time
            try:
                query = f"INSERT INTO db_projn.noticias (url,titulo, imgsrc, data, fonte, autor) VALUES (%s, %s, %s, %s, %s, %s);"
                cursor.execute(query, (article_link,article_title,img_src,result_string, 'Poder360', article_author))
                connection.commit()
                print(article_title)
                print(article_author)
                print(article_link)
                print(result_string) #date
                print(img_src)
                print(i)
            except Exception as e:
                # Handle other exceptions
                print(f"An unexpected error occurred:{i} \n{e}")
            
    else:
        print(f"\n\nFailed to fetch the page. Status code: {response.status_code}\n\n")

if __name__ == "__main__":
    # Replace this URL with the website you want to scrape
    target_url = "https://www.poder360.com.br/poder-hoje/"
    
    # Call the function with the target URL
    scrape_news(target_url)
    # Close the cursor and connection
    cursor.close()
    connection.close()