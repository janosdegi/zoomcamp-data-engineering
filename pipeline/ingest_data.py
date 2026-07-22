import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm

dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

def ingest_data():

    target_table = 'yellow_taxi_data'
    year = 2021
    month = 1

    engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')

    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    url = f'{prefix}/yellow_tripdata_{year:04d}-{month:02d}.csv.gz'

    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=100000)

    first = True
    for df_chunk in tqdm(df_iter):
        if first:
            #create table
            df_chunk.head(0).to_sql(name=target_table, con=engine, if_exists='replace')
            first = False
        df_chunk.to_sql(name=target_table, con=engine, if_exists='append')


if __name__ == '__main__':
    ingest_data()