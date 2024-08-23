import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.firefox import GeckoDriverManager
from itertools import combinations

# Function to fetch articles from Financial Times
def fetch_ft_articles(keywords, num_links):
    base_search_url = 'https://www.ft.com/search?sort=relevance&q='
    search_query = '+'.join(keyword.replace(' ', '+') for keyword in keywords)
    search_url = base_search_url + search_query

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(search_url, headers=headers)
    response.raise_for_status()
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')
    articles = []

    for article in soup.find_all('div', class_='o-teaser__heading')[:num_links]:
        link = article.find('a')
        if link:
            title = link.get_text(strip=True)
            url = 'https://www.ft.com' + link['href']
            articles.append({'title': title, 'url': url})

    return articles

# Function to fetch article URLs from Bloomberg
def fetch_bloomberg_article_urls(keywords, num_links):
    base_search_url = 'https://www.bloomberg.com/search?query='
    search_query = '%20'.join(keyword.replace(' ', '%20') for keyword in keywords)
    search_url = base_search_url + search_query

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
    ]

    firefox_options = Options()
    firefox_options.add_argument("--headless")
    firefox_options.add_argument("--disable-gpu")
    firefox_options.add_argument("--no-sandbox")
    firefox_options.add_argument("--disable-dev-shm-usage")
    firefox_options.add_argument("--window-size=1920x1080")
    firefox_options.add_argument(f"user-agent={random.choice(user_agents)}")

    urls = []

    try:
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=firefox_options)

        driver.get(search_url)
        time.sleep(random.uniform(5, 10))

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class^="storyItem"]'))
        )

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        for article in soup.find_all('div', class_=lambda x: x and x.startswith('storyItem'))[:num_links]:
            link = article.find('a', href=True)
            if link:
                url = link['href']
                if not url.startswith('https://'):
                    url = 'https://www.bloomberg.com' + url
                urls.append(url)

        driver.quit()
        return urls[:num_links]

    except Exception as e:
        driver.quit()
        return []

# Function to fetch article titles from Bloomberg URLs
def fetch_bloomberg_articles(urls):
    articles = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for url in urls:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        html = response.text

        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('title').get_text(strip=True)
        articles.append({'title': title, 'url': url})

    return articles

def get_combinations(keywords, r):
    return list(combinations(keywords, r))

# Streamlit web application
st.title("Good Morning Sir")
st.write("Please enter the number of keywords you want to search for (up to 10):")
num_keywords = st.slider("Number of Keywords", 1, 10, 3)

keywords = []
for i in range(1, num_keywords + 1):
    keyword = st.text_input(f"Keyword {i}", key=f"keyword_{i}")
    if keyword:
        keywords.append(keyword)

num_links = st.slider("How many links to show?", 1, 30, 10)

if st.button("Fetch Articles"):
    if keywords:
        st.write(f"Fetching top {num_links} articles for keywords: {', '.join(keywords)}")

        # Fetch articles from Financial Times
        st.write("### Financial Times Articles")
        ft_articles = fetch_ft_articles(keywords, num_links)
        for i, article in enumerate(ft_articles, start=1):
            st.write(f"{i}. [{article['title']}]({article['url']})")

        # Fetch articles from Bloomberg with different combinations
        st.write("### Bloomberg Articles")
        bloomberg_urls = []
        for r in range(len(keywords), 0, -1):
            if len(bloomberg_urls) >= num_links:
                break
            keyword_combinations = get_combinations(keywords, r)
            for combo in keyword_combinations:
                if len(bloomberg_urls) >= num_links:
                    break
                try:
                    bloomberg_urls += fetch_bloomberg_article_urls(combo, num_links - len(bloomberg_urls))
                except Exception as e:
                    st.write(f"Error fetching articles for combination {combo}: {e}")

        bloomberg_articles = fetch_bloomberg_articles(bloomberg_urls)
        for i, article in enumerate(bloomberg_articles, start=1):
            st.write(f"{i}. [{article['title']}]({article['url']})")
    else:
        st.write("Please enter at least one keyword.")
