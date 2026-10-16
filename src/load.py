import duckdb
import logging
from pathlib import Path


Path('./db').mkdir(exist_ok=True)
Path('./logs').mkdir(exist_ok=True)

logging.basicConfig(level=logging.INFO,
                    filename='./logs/load.log',
                    filemode='w',
                    format='%(asctime)s %(levelname)s %(message)s')

parquet_path = './data/processed/books_clean.parquet'

try:
    con = duckdb.connect('./db/books.db')
    con.execute(
        f"CREATE OR REPLACE TABLE books AS "
        f"SELECT * FROM '{parquet_path}'"
    )

    cnt = con.query('SELECT COUNT(*) FROM books').fetchone()[0]
    if cnt == 0:
        logging.warning('Table books is empty!')
    else:
        logging.info(f'Loaded {cnt} rows into books.db')

    con.close()
except FileNotFoundError:
    logging.error('Parquet file not found')
except Exception as err:
    logging.error(f'Load error: {err}')
