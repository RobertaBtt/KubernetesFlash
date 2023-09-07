from flask import Blueprint, Response, request
from .DependencyContainer import DependencyContainer
import json
import requests
from . import errors

main = Blueprint("app", __name__)
container = DependencyContainer()
service_csv = container.service_csv()

"""Treating the CSV as a subentity of topic"""


@main.route('/topic/<string:topic>/csv/')
def csv_by_topic(topic):

    csv_list = service_csv.get_csv_by_topic({'%TOPIC%': topic})

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

    try:

        csv = service_csv.get_csv_by_id({'%ID%': id})
    except errors.ERRORS['OperationalError'] as ex:
        response = Response(str(ex), status=503, mimetype="application/json")
        return response

    if csv is not None:
        url = csv[1]

    else:
        response = Response(status=404, mimetype="application/json")
        return response

    query_parameters = {"downloadedformat": "csv"}
    response = requests.get(url, params=query_parameters)

    with open("temp_file.csv", mode="wb") as file:
        # Since we just need the header, I don't save the entire file,
        # but just one chunk of 1kb, enough to contain
        # the header even for files with 100 columns
        for chunk in response.iter_content(chunk_size=1024):
            file.write(chunk)
            break

    with open('temp_file.csv') as f:
        csv_header = f.readline().strip('\n')

    data = json.dumps(csv_header)
    response = Response(data, status=200, mimetype="application/json")
    response.headers["Content-Type"] = "text/json; charset=utf-8"
    return response


@main.route('/csv', methods=['POST'])
def add_csv():
    record = json.loads(request.data)

    try:
        service_csv.add_csv({
            '%URL%': record['url'],
            '%TOPIC%': record['topic']
        })

    except errors.ERRORS['OperationalError'] as ex:
        response = Response(str(ex), status=503, mimetype="application/json")
        return response

    response = Response( status=200, mimetype="application/json")
    response.headers["Content-Type"] = "text/json; charset=utf-8"
    return response


@main.route('/')
def index():
    return 'App Works!'
