import requests
from bs4 import BeautifulSoup

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
        latest_articles_html = soup.find_all('div', 'feed-post-body-title')
        i = 0
        # Print the titles of the articles
        for latest in latest_articles_html:
            i += 1
            #print(latest)
            article_title_html = latest.find('h2')
            article_title = article_title_html.text
            article_link_html = latest.find('a')
            article_link = article_link_html.get('href')
            article_timestamp = scrape_time(article_link)
            if(article_timestamp == -1): print('failed to get timestamp')
            else:
                print(i)
                print(article_title)
                print(article_link)
                print(article_timestamp)
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")

if __name__ == "__main__":
    # Replace this URL with the website you want to scrape
    economia_url = "https://oglobo.globo.com/economia/"
    politica_url = "https://oglobo.globo.com/politica/"
    
    scrape_news(economia_url)
    scrape_news(politica_url)