import sqlite3
import pandas as pd
from pathlib import Path

conn = sqlite3.connect(
    "EHR2000.db"
)  # Connect (and create if it doesn't exist) database
cursor = conn.cursor()  # Object to run queries


path = Path("../EHRShot_sampled_2000patients/")
chunksize = 10**7

for f in Path.iterdir(path):
    if not f.is_file():
        continue
    csv_file = f.relative_to(".")  # make the path relative to the script
    table_name = f.name.split(".")[0]  # only use file name, not extension (.csv)
    with pd.read_csv(csv_file, chunksize=chunksize) as reader:
        for chunk in reader:
            chunk.to_sql(table_name, conn, if_exists="append", index=False)
            print(f"Chunk written from: {f.name} to table: {table_name}")
        print("-" * 50)
        print(f"Converted file: {f.name} to table: {table_name}")
        print("-" * 50)


conn.close()
