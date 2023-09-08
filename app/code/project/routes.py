from flask import Blueprint, Response, request
from .DependencyContainer import DependencyContainer
from werkzeug.exceptions import HTTPException
from socket import error as  socket_error

import json
import requests
from . import errors

main = Blueprint("app", __name__)
container = DependencyContainer()
service_csv = container.service_csv()

@main.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


def handle_response(response_dictionary):
    data = json.dumps(response_dictionary)
    response = Response()
    response.data = data
    response.content_type = "application/json"
    return response


@main.route('/topic/<string:topic>/csv/')
def csv_by_topic(topic):
    try:
        csv_list = service_csv.get_csv_by_topic({'%TOPIC%': topic})
    except errors.ERRORS['OperationalError']:
        exp = errors.OperationalError()
        return handle_exception(exp)
    except Exception as ex:
        return handle_exception(ex)

    response_dictionary = dict(topic=topic, csv=csv_list)
    return handle_response(response_dictionary)


@main.route('/csv/<csv_id>/')
def csv_by_id(csv_id):

    try:
        isinstance(int(csv_id),int)
    except ValueError:
        exp = errors.BadParameter()
        return handle_exception(exp)

    try:
        csv = service_csv.get_csv_by_id({'%ID%': csv_id})
    except errors.ERRORS['OperationalError']:
        exp = errors.OperationalError()
        return handle_exception(exp)
    except Exception as ex:
        return handle_exception(ex)

    if csv is not None:
        url = csv[1]
    else:
        resource_not_found = errors.ResourceNotFound()
        return handle_exception(resource_not_found)

    try:
        response = requests.get(url, params={"downloadedformat": "csv"})
    except Exception as ex:
        return handle_exception(ex)

    if response.status_code == 404:
        exp = errors.NameResolutionError()
        return handle_exception(exp)

    file_name = url.split("/")[-1]

    container.downloader(file_name, response)

    with open(file_name) as f:
        csv_header = f.readline().strip('\n')

    response_dictionary = {'headers': csv_header}
    return handle_response(response_dictionary)



@main.route('/csv', methods=['POST'])
def add_csv():
    record = json.loads(request.data)

    if 'url' not in record or 'topic' not in record:
        exp = errors.MissingParameters()
        return handle_exception(exp)

    url = record['url']
    try:
        service_csv.add_csv({
            '%URL%': record['url'],
            '%TOPIC%': record['topic']
        })

        csv = service_csv.get_csv_by_url({'%URL%': url})

    except errors.ERRORS['OperationalError']:
        exp = errors.OperationalError()
        return handle_exception(exp)
    except errors.ERRORS['IntegrityError']:
        exp = errors.IntegrityError()
        return handle_exception(exp)
    except Exception as ex:
        return handle_exception(ex)

    response_dictionary = {'data': csv}
    return handle_response(response_dictionary)


@main.route('/')
def index():
    return 'App Works!'
