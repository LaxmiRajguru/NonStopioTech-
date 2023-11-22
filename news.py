#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install request


# In[2]:


pip install requests


# In[5]:


pip install beautifulsoup4


# In[10]:


pip install html5lib


# In[14]:


pip install urllib3
pip install beautifulsoup4


# In[15]:


get_ipython().system('pip install beautifulsoup4')
get_ipython().system('pip install urllib3')


# In[35]:


from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd

root = "https://www.google.com/"
link = "https://www.google.com/search?q=biden&tbm=nws&source=lnt&tbs=sbd:1&sa=X&ved=0ahUKEwjAvsKDyOXtAhXBhOAKHXWdDgcQpwUIKQ&biw=1604&bih=760&dpr=1.2"

def scrape_google_news(link, limit=100):
    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage,'html.parser')

    data = []

    for item in soup.find_all('div', attrs={'class': 'ZINbbc xpd O9g5cc uUPGi'}):
        raw_link = (item.find('a', href=True)['href'])
        link = (raw_link.split("/url?q=")[1]).split('&sa=U&')[0]
                
        title = (item.find('div', attrs={'class': 'BNeawe vvjwJb AP7Wnd'}).get_text())
        description = (item.find('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'}).get_text())

        title = title.replace(",", "")
        description = description.replace(",", "")

        time = description.split(" · ")[0]
        descript = description.split(" · ")[1]
 
        classification = item.find('span', attrs={'class': 'classification-class'}).get_text()

        data.append([title, time, descript, link, classification])

        if len(data) >= limit:
            break

    return data

def save_to_csv(data, filename="C:/Users/LAXMI/Data.csv"):
    df = pd.DataFrame(data, columns=["Title", "Time", "Description", "Link", "Classification"])
    df.to_csv(filename, mode='a', header=not pd.read_csv(filename).empty, index=False)

def news(link):
    data = scrape_google_news(link, limit=100)
    save_to_csv(data)

    next_page = soup.find('a', attrs={'aria-label': 'Next page'})
    if next_page:
        next_link = root + next_page['href']
        news(next_link)

# Run the scraping and save to CSV
news(link)


# In[42]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

article_list = []

def get_soup(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def get_articles(soup):
    articles = soup.find_all('div', {'class': 'article-headline-container'})  
    try:
        for article in articles:
           
            title = article.find('h2').text.strip()
            body = article.find('div', {'class': 'article-body'}).text.strip()
           
            article_data = {
                'title': title,
                'body': body,
            }
            article_list.append(article_data)
    except Exception as e:
        print(f"An error occurred: {e}")

for page_number in range(1, 6):  
    url = f'https://timesofindia.indiatimes.com/page/{page_number}' 
    soup = get_soup(url)
    print(f'Getting page: {page_number}')
    get_articles(soup)
    print(len(article_list))

df = pd.DataFrame(article_list)
df.to_csv('times_of_india_articles.csv', index=False)  # Save to CSV
print('Scraping and CSV saving completed.')


# In[54]:


from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import quote

root = "https://www.bing.com/"
query = "news music"
link = f"https://www.bing.com/news/search?q={quote(query)}"

# Rest of the code remains the same

def scrape_bing_news(link):
    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'html.parser')

    news_articles = soup.find_all('div', class_='news-card newsitem cardcommon')

    data = []

    for article in news_articles:
        # Extract information from each article
        title_tag = article.find('h2')
        link_tag = article.find('a')
        description_tag = article.find('p')

        if title_tag and description_tag and link_tag:
            title = title_tag.text.strip()
            description = description_tag.text.strip()
            link = link_tag['href'].strip()

            data.append({'Title': title, 'Description': description, 'Link': link})

    return data

# Call the function to scrape Bing news
scraped_data = scrape_bing_news(link)

# Create a DataFrame
df = pd.DataFrame(scraped_data)

# Save DataFrame to a CSV file
df.to_csv('bing_news_data.csv', index=False)

print("Data saved to CSV successfully.")


# In[ ]:




