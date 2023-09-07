from flask import Blueprint, Response, request, abort
from .DependencyContainer import DependencyContainer
from werkzeug.exceptions import HTTPException
import json
import requests
from . import errors

main = Blueprint("app", __name__)
container = DependencyContainer()
service_csv = container.service_csv()

"""Treating the CSV as a subentity of topic"""

"""Get the list of the CSV registered in the system, by the topic"""


@main.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
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


@main.route('/csv/<id>/')
def csv_by_id(id):

    try:
        isinstance(int(id),int)
    except ValueError as ex:
        exp = errors.BadParameter()
        return handle_exception(exp)

    try:
        csv = service_csv.get_csv_by_id({'%ID%': id})
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

    response_dictionary = {'headers': csv_header}
    return handle_response(response_dictionary)



@main.route('/csv', methods=['POST'])
def add_csv():
    record = json.loads(request.data)

    if 'url' not in record or 'topic' not in record:
        exp = errors.MissingParameters()
        return handle_exception(exp)

    try:
        service_csv.add_csv({
            '%URL%': record['url'],
            '%TOPIC%': record['topic']
        })

    except errors.ERRORS['OperationalError']:
        exp = errors.OperationalError()
        return handle_exception(exp)
    except errors.ERRORS['IntegrityError']:
        exp = errors.IntegrityError()
        return handle_exception(exp)
    except Exception as ex:
        return handle_exception(ex)

    response_dictionary = {'data': record}
    return handle_response(response_dictionary)


@main.route('/')
def index():
    return 'App Works!'
