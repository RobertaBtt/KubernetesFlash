import os
from flask import Blueprint, Response
import json
import requests
import csv

main = Blueprint("app", __name__)

# API_KEY = os.environ['API_KEY']

"""Treating the CSV as a subentity of topic"""


@main.route('/topic/<string:topic>/csv/')
def csv_by_topic(topic):

    csv_list = []
    csv_list.append('https://vincentarelbundock.github.io/Rdatasets/csv/AER/ArgentinaCPI.csv')
    csv_list.append('https://vincentarelbundock.github.io/Rdatasets/csv/AER/CPS1985.csv')

    response_dict = dict(
        topic=topic,
        csv=csv_list
    )
    data = json.dumps(response_dict)

    response = Response(data, status=200, mimetype="application/json")
    response.headers["Content-Type"] = "text/json; charset=utf-8"
    return response


@main.route('/csv/<id>/')
def csv_by_id(id):

    url = 'https://vincentarelbundock.github.io/Rdatasets/csv/AER/ArgentinaCPI.csv'
    url = "https://vincentarelbundock.github.io/Rdatasets/csv/causaldata/mortgages.csv" #214 mila record
    url = "https://vincentarelbundock.github.io/Rdatasets/csv/wooldridge/loanapp.csv" # 58 colonne
    url = "https://vincentarelbundock.github.io/Rdatasets/csv/tidyr/billboard.csv" # 79 colonne

    query_parameters = {"downloadedformat": "csv"}

    response = requests.get(url, params=query_parameters)

    with open("temp_file.csv", mode="wb") as file:
        # Since we just need the header, I don't save the entire file,
        # but just one chunk of 1kb, enough to contain
        # the header even for files with 100 columns
        for chunk in response.iter_content(chunk_size=1024):
            file.write(chunk)
            break

    with open('temp_file.csv', newline='') as f:
        csv_reader = csv.reader(f)
        csv_header = next(csv_reader)

    data = json.dumps(csv_header)
    response = Response(data, status=200, mimetype="application/json")
    response.headers["Content-Type"] = "text/json; charset=utf-8"
    return response

@main.route('/')
def index():
    return 'App Works!'
