import sys

import requests
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from tabulate import tabulate

def fetch_ft_articles(keywords, num_links=5):
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

    return articles[:num_links]

def analyze_sentiment(articles):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = []

    for article in articles:
        sentiment = analyzer.polarity_scores(article['title'])
        sentiment_scores.append(sentiment['compound'])

    if sentiment_scores:
        average_sentiment = sum(sentiment_scores) / len(sentiment_scores)
        return average_sentiment
    else:
        return 0

def investment_advice(sentiment_score):
    if sentiment_score > 0.05:
        return "Good day to invest"
    elif sentiment_score < -0.05:
        return "Bad day to invest"
    else:
        return "Neutral sentiment, invest with caution"

if __name__ == "__main__":
    sector_stocks = {
        "Technology": ["NVIDIA", "Apple", "Microsoft"],
        "Energy": ["Exxon Mobil", "Chevron"],
        "Utilities": ["Duke Energy", "NextEra Energy"],
        "Consumer Discretionary": ["Amazon", "Tesla"],
        "Materials": ["BHP Group", "Rio Tinto"],
        "Real Estate": ["Simon Property Group", "Prologis"],
        "Industrials": ["Boeing", "Caterpillar"],
        "Financials": ["JPMorgan Chase", "Goldman Sachs"],
        "Consumer Staples": ["Procter & Gamble", "Coca-Cola"],
        "Health Care": ["Pfizer", "Johnson & Johnson"]
    }

    num_links = 5  # Number of articles to fetch per stock

    data = {sector: [] for sector in sector_stocks}

    max_len = 0
    for sector, stocks in sector_stocks.items():
        for stock in stocks:
            articles = fetch_ft_articles([stock], num_links)
            sentiment_score = analyze_sentiment(articles)
            advice = investment_advice(sentiment_score)
            data[sector].append(f"{stock}: {sentiment_score:.2f} ({advice})")
        max_len = max(max_len, len(stocks))

    # Create a DataFrame from the dictionary
    for sector in data:
        data[sector] += [""] * (max_len - len(data[sector]))  # Padding with empty strings

    df = pd.DataFrame(data)

    # Print the DataFrame using the tabulate library for better formatting
    print(tabulate(df, headers='keys', tablefmt='grid'))
