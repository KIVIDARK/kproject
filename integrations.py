import requests
import json

from requests.auth import HTTPBasicAuth


def mailjet_integration_handler(request, integration):
    """
    Simple API client for mailjet.com.
    Creates a user with specified name and email, and puts him into the list

    Integration object should include:
    - api_key - api key for mailjet.com API
    - secret_key - secret key for mailjet.com API
    - list ID - list ID for adding contact in mailjet.com API

    :param request: standard django request object with a custom user object
    :param integration: defined in the admin panel and populated from the client business console based on
    the variable data needed to complete an API task
    :return: dictionary of request data, response data, request url
    """

    api_key = integration.parameters.get(name='api_key').value
    secret_key = integration.parameters.get(name='secret_key').value
    list_id = integration.parameters.get(name='list_id').value

    api_url = "https://api.mailjet.com/v3/REST/contactslist/{}/ManageManyContacts".format(list_id)

    data = {
        "Action": "addnoforce",
        "Contacts": [
            {
                "Email": request.user.email,
                "Properties": {
                        "FirstName": request.user.first_name,
                        "Name": request.user.last_name
                }
            }
        ]
    }

    response = requests.post(
        api_url,
        auth=HTTPBasicAuth(api_key, secret_key),
        headers={
            'content-type': 'application/json'
        },
        data=json.dumps(data)
    )

    result = {
        'r': response.text,
        'data_sent': data,
        'api_url': api_url
    }

    return result


def mailerlite_integration_handler(request, integration):
    """
    Simple API client for mailerlite.com.
    Creates a user with specified name and email, and puts him into the list

    Integration object should include:
    - api_key - api key for mailerlite.com API
    - group - group for adding subscriber in mailerlite.com API

    :param request: standard django request object with a custom user object
    :param integration: defined in the admin panel and populated from the client business console based on
    the variable data needed to complete an API task
    :return: dictionary of request data, response data, request url
    """

    api_key = integration.parameters.get(name='api_key').value
    group = integration.parameters.get(name='group').value

    base_url = "https://api.mailerlite.com/api/v2/"
    create_url = base_url + "groups/{}/subscribers".format(group)

    data = {
        "email": request.user.email,
        "name": request.user.first_name,
        "fields": {
            "last_name": request.user.last_name
        }
    }

    headers = {
        'content-type': "application/json",
        'x-mailerlite-apikey': api_key
    }

    response = requests.post(create_url, data=json.dumps(data), headers=headers)

    result = {
        'r': response.text,
        'data_sent': data,
        'api_url': create_url
    }

    return result


def ontraport_integration_handler(request, integration):
    """
    Simple API client for ontraport.com.
    Creates a user with specified name and email, and puts him into the list

    Integration object should include:
    - api_key - API key for ontraport.com API
    - api_app_id - API App ID for ontraport.com API

    :param request: standard django request object with a custom user object
    :param integration: defined in the admin panel and populated from the client business console based on
    the variable data needed to complete an API task
    :return: dictionary of request data, response data, request url
    """

    api_key = integration.parameters.get(name='api_key').value
    api_app_id = integration.parameters.get(name='api_app_id').value

    api_url = "https://api.ontraport.com/1/objects"

    data = {
        "objectID": 0,
        "email": request.user.email,
        "firstname": request.user.first_name,
        "lastname": request.user.last_name
    }

    headers = {
        'Content-Type': "application/json",
        'Accept': 'text/html',
        'Api-Key': api_key,
        'Api-Appid': api_app_id
    }

    response = requests.post(api_url, data=json.dumps(data), headers=headers)

    result = {
        'r': response.text,
        'data_sent': data,
        'api_url': api_url
    }

    return result
