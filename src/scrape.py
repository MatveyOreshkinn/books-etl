import logging
from pathlib import Path
import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException


Path('./data/raw').mkdir(parents=True, exist_ok=True)
Path('./logs').mkdir(exist_ok=True)

url = 'https://books.toscrape.com/catalogue/'

logging.basicConfig(level=logging.INFO, filename='./logs/scrape.log', filemode='w', format='%(asctime)s %(levelname)s %(message)s')

for i in range(1, 51):
    try:
    
        filename = f'page-{i}.html'
        response = requests.get(url + filename, timeout=10)
        response.raise_for_status()
        
        encoding = response.apparent_encoding
        with open(f'./data/raw/books_page_{i}.html', 'w', encoding=encoding) as file: 
            file.write(response.text)
            logging.info(f'Page={i}: Success')

    except HTTPError as http_err:
        logging.error(f'Page={i}: HTTP error occurred: {http_err}')
    except ConnectionError as conn_err:
        logging.error(f'Page={i}: Connection error occurred: {conn_err}')
    except Timeout as timeout_err:
        logging.error(f'Page={i}: Timeout error occurred: {timeout_err}')
    except RequestException as req_err:
        logging.error(f'Page={i}: Unexpected error occurred: {req_err}')
