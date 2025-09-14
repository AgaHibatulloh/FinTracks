from sqlalchemy import create_engine, Table, Column, Integer, String, Float, MetaData
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/fintrack")
engine = create_engine(DATABASE_URL)
metadata = MetaData()

finance_table = Table(
    "finance", metadata,
    Column("id", Integer, primary_key=True),
    Column("month", String),
    Column("revenue", Float),
    Column("expense", Float),
    Column("embedding", String),  # sementara simpan string json
)

metadata.create_all(engine)

def insert_financial_data(df):
    with engine.begin() as conn:
        records = df.to_dict(orient="records")
        conn.execute(finance_table.insert(), records)