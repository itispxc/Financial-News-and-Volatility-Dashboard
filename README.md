# Financial News and Volatility Dashboard

This Streamlit web application allows users to search for the latest news articles from Financial Times and Bloomberg using specified keywords. It also analyzes market sector volatility using Yahoo Finance data.
<img width="515" alt="Screenshot 2024-08-08 at 12 01 36 AM" src="https://github.com/user-attachments/assets/54608700-8cba-423d-8b9f-206dc3ecdf5f">

<img width="423" alt="Screenshot 2024-08-08 at 12 01 16 AM" src="https://github.com/user-attachments/assets/18a8d100-bdfe-4100-a019-e0acf7bbfd26">


## Features

- **Article Fetching**: 
  - **Financial Times**: Uses `requests` and **BeautifulSoup** to scrape article titles and URLs based on user-input keywords.
  - **Bloomberg**: Employs **Selenium WebDriver** to dynamically load and extract article URLs. Parses the titles directly from the URLs.

- **Volatility Analysis**:
  - Computes annualized volatility for selected market sectors (e.g., Energy, Technology) using historical data from Yahoo Finance.
  - Presents a ranked list of sectors by volatility.

- **Dynamic Greeting**:
  - Displays a personalized greeting based on the current time in Hong Kong.

## Usage

1. **Keyword Input**: Enter up to 10 keywords.
2. **Link Selection**: Choose the number of article links to display.
3. **Fetch Articles**: Click to retrieve and view the latest news from Financial Times and Bloomberg.
4. **Volatility Check**: View the most volatile sectors in a descending order.

## Technologies Used

- **Streamlit**: For creating the user interface and handling user interactions.
- **Requests & BeautifulSoup**: For efficiently scraping and parsing HTML content from Financial Times.
- **Selenium**: For automating browser actions to scrape dynamic Bloomberg content.
- **Yahoo Finance (yfinance)**: For accessing and analyzing historical market data.
- **Python Libraries**: Utilizes `itertools` for keyword combinations, `datetime` and `pytz` for time-based features.

## Note

Ensure you have the following dependencies installed: `streamlit`, `requests`, `beautifulsoup4`, `selenium`, `yfinance`, and `webdriver-manager`.


