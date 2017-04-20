import requests
import json
import sys

from requests.auth import HTTPBasicAuth

if sys.version_info[0] < 3:
    from urllib import urlencode
else:
    from urllib.parse import urlencode


def hubspot_integration_handler(request, integration):
    """
    Simple API client for hubspot.com.
    Creates a user with specified name and email, and puts him into the list

    Integration object should include:
    - api_key - hapikey for hubspot.com API

    :param request: standard django request object with a custom user object
    :param integration: defined in the admin panel and populated from the client business console based on
    the variable data needed to complete an API task
    :return: dictionary of request data, response data, request url
    """

    api_key = integration.parameters.get(name='api_key').value

    params = {
        "hapikey": api_key
    }

    data = {
        "properties": [
            {
              "property": "email",
              "value": request.user.email
            },
            {
              "property": "firstname",
              "value": request.user.first_name
            },
            {
              "property": "lastname",
              "value": request.user.last_name
            },
        ]
    }

    base_url = "https://api.hubapi.com/contacts/v1/"
    create_url = base_url + "contact/"

    response = requests.post(create_url, data=json.dumps(data), params=urlencode(params)).text

    result = {
        'r': response,
        'data_sent': data,
        'api_url': create_url
    }

    return result


def highrise_integration_handler(request, integration):
    """
    Simple API client for highrisehq.com.
    Creates a user with specified name and email, and puts him into the list

    Integration object should include:
    - api_key - token for highrisehq.com API
    - company - company name for highrisehq.com API

    :param request: standard django request object with a custom user object
    :param integration: defined in the admin panel and populated from the client business console based on
    the variable data needed to complete an API task
    :return: dictionary of request data, response data, request url
    """

    api_key = integration.parameters.get(name='api_key').value
    company = integration.parameters.get(name='company').value

    params = {}

    data = """<?xml version='1.0' encoding='utf-8'?>
    <person>
        <first_name>{}</first_name>
        <last_name>{}</last_name>
        <contact-data>
            <email_addresses>
                <email-address>
                    <address>{}</address>
                </email-address>
            </email_addresses>
        </contact-data>
    </person>""".format(request.user.first_name, request.user.last_name, request.user.email)

    api_url = 'https://{}.highrisehq.com/people.xml'.format(company, params)

    response = requests.post(
        api_url,
        auth=HTTPBasicAuth(api_key, "X"),
        headers={
            'User-Agent': '',
            'content-type': 'application/xml'
        },
        params=params,
        data=data
    )

    result = {
        'r': response.text,
        'data_sent': data,
        'api_url': api_url
    }

    return result
