from bs4 import BeautifulSoup
import pandas as pd
import logging
from pathlib import Path


Path('./data/parsed').mkdir(exist_ok=True)

all_data = []
logging.basicConfig(level=logging.INFO,
                    filename='./logs/parser.log',
                    filemode='w',
                    format='%(asctime)s %(levelname)s %(message)s')

for i in range(1, 51):
    try:
        with open(f'./data/raw/books_page_{i}.html') as file:
            soup = BeautifulSoup(file, 'html.parser')
            articles = soup.find_all('article')

            title_col = []
            rating_col = []
            price_col = []
            instock_col = []

            for article in articles:
                title = article.find('h3').find('a')['title']
                rating = article.find('p', class_='star-rating')['class'][1]
                price = article.find('p', class_='price_color').text[4:]
                instock = article.find('p', class_='instock').text.strip()

                title_col.append(title)
                rating_col.append(rating)
                price_col.append(price)
                instock_col.append(instock)

            parsed_data = pd.DataFrame({'Title': title_col,
                                        'Rating': rating_col,
                                        'Price': price_col,
                                        'In stock': instock_col})
            all_data.append(parsed_data)

            logging.info(f'Page={i}: Success')

    except FileNotFoundError:
        logging.error(f'Page={i}: file not found')
    except Exception as err:
        logging.error(f'Page={i}: error: {err}')

result = pd.concat(all_data, ignore_index=True)
result.to_csv('./data/parsed/books.csv', mode='w', index=False, header=True)
