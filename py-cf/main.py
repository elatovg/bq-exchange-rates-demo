from google.cloud import storage
from google.cloud import bigquery
from datetime import date
from flask import escape
import json
import os

def run_cf(request):
    if (request == "local"):
        if 'QUERY_DATE' in os.environ:
            qdate = os.environ.get('QUERY_DATE')
        else:
            today = date.today()
            qdate = today.strftime("%Y-%m-%d")
    else:
        request_json = request.get_json(silent=True)
        request_args = request.args

        if request_json and 'query_date' in request_json:
            qdate = request_json['query_date']

    # download json from gcs
    bucket_name = os.environ.get('BUCKET_NAME')
    json = download_json(qdate, bucket_name)

    # add data into bq
    bq_dataset = os.environ.get('BQ_DATASET')
    bq_table = os.environ.get('BQ_TABLE')
    insert_into_bq(qdate,json,bq_dataset,bq_table)

def download_json(qdate, bucket_name):
    # prep to download the file
    folder_name = "exchange-rates"
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    file_name = "{}/{}.json".format(folder_name,qdate)

    # download the file from gcs
    blob = bucket.blob(file_name)

    # read the json into a python dictionary
    data = json.loads(blob.download_as_string(client=None))

    # for debugging
    # print(data)

    return(data)

def insert_into_bq(qdate, json, bq_dataset, bq_table):
    # prepare the data
    usd,cad,mxn,gbp,cny = (json['rates']['USD'],
                            json['rates']['CAD'],
                            json['rates']['MXN'],
                            json['rates']['GBP'],
                            json['rates']['CNY']
    )
    row = [(qdate,usd,cad,mxn,gbp,cny)]

    print(row)
    
    # prepare the bq client
    bq_client = bigquery.Client()
    table_id = "{}.{}".format(bq_dataset, bq_table)
    table = bq_client.get_table(table_id)

    # data to insert
    # rows_to_insert = [(u"Phred Phlyntstone", 32), (u"Wylma Phlyntstone", 29)]

    # try to insert the data
    errors = bq_client.insert_rows(table, row) 
    # errors = client.insert_rows(table, rows_to_insert)  # Make an API request.

    # errors = BQ.insert_rows_json(table,json_rows=[row],
    #                     row_ids=[file_name],retry=retry.Retry(deadline=30))

    if errors == []:
        print("New rows have been added.")

# for debugging locally
if __name__ == "__main__":
    request = "local"
    run_cf(request)