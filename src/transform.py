import pandas as pd
from pathlib import Path
import logging


Path('./data/processed').mkdir(parents=True, exist_ok=True)
Path('./logs').mkdir(exist_ok=True)
logging.basicConfig(level=logging.INFO,
                    filename='./logs/transform.log',
                    filemode='w',
                    format='%(asctime)s %(levelname)s %(message)s')

rating = {'One': 1,
          'Two': 2,
          'Three': 3,
          'Four': 4,
          'Five': 5}
try:
    df = pd.read_csv('./data/parsed/books.csv')
    logging.info('Load csv success')

    df['Rating'] = df['Rating'].map(rating)

    df['In stock'] = df['In stock'].apply(
        lambda x: 1 if 'In stock' in x else 0
    )

    df['Title'] = df['Title'].str.strip()
    df['Title'] = df['Title'].str.replace(r'\s+', ' ', regex=True)

    df['In stock'] = df['In stock'].astype('bool')
    df['Price'] = df['Price'].astype(float)

    df.drop_duplicates(subset=['Title'], inplace=True)
    df.dropna(inplace=True)

    logging.info('Preprocessing success')

    df.to_parquet('./data/processed/books_clean.parquet', index=False)
    logging.info('Save parquet success')

except FileNotFoundError:
    logging.error('File not found')
except Exception as err:
    logging.error(f'Occured error: {err}')
