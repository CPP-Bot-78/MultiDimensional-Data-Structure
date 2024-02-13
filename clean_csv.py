import pandas as pd
import os


script_directory = os.path.dirname(os.path.abspath(__file__))
home_dir = os.path.dirname(script_directory)
CSV_PATH = os.path.join(script_directory, 'computer_scientists_data1.csv')
df = pd.read_csv(CSV_PATH)
# df = df.drop_duplicates(subset=df.columns[1])
df = df[~df.duplicated(subset=df.columns[1], keep='first')]
df = df.drop(df.columns[0], axis=1)
df = df.reset_index(drop=True)
df.to_csv('computer_scientists_data2.csv', index=True)
