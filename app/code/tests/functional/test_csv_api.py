
"""
GIVEN a Flask application configured for testing
WHEN the '/' page is requested (GET)
THEN response is valid
THEN output is valid
"""


def test_home_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"App Works!" in response.data


def test_csv_by_topic(test_client):
    topic_test = "software"
    response = test_client.get(f'/topic/{topic_test}/csv/')
    assert response.status_code == 200
    assert b"topic" in response.data


def test_csv_by_id(test_client):
    csv_id = "29384"
    response = test_client.get(f'/csv/{csv_id}/')
    assert response.status_code == 200
    assert b'["rownames", "time", "value"]' in response.data

