from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine

DB_PATH = Path(__file__).resolve().parents[1] / 'bitita_web.db'
engine = create_engine(f'sqlite:///{DB_PATH}')

query = "SELECT * FROM students"

df = pd.read_sql_query(query, engine)

if df.empty:
    print('Nenhum dado encontrado para análise.')
else:
    print('\nResumo dos estudantes:')
    print(df[['name', 'nationality', 'generation', 'accommodation']].head())
    print('\nQuantidade por nacionalidade:')
    print(df['nationality'].value_counts())
