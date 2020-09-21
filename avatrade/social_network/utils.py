from django.apps import apps
import clearbit
import requests
import json

APP_LABEL = 'social_network'

HUNTER_EMAIL_VERIFIED = 'deliverable'
HUNTER_EMAIL_NOT_VERIFIED = 'undeliverable'
HUNTER_EMAIL_VERIFICATION_FAILURE = 'risky'


def verify_email(email):
    hunter = apps.get_app_config(APP_LABEL).hunter
    url = f'{hunter["url"]}/email-verifier'
    response = requests.get(url, {'email': email, 'api_key': hunter["key"]})

    if response.ok:
        data = json.loads(response.content)
        result = data['data']['result']
        if result == HUNTER_EMAIL_VERIFICATION_FAILURE:
            raise RuntimeError(f'Hunter has failed to validate {email}')
        return result == HUNTER_EMAIL_VERIFIED
    else:
        response.raise_for_status()


def enrich_by_email(email):
    config = apps.get_app_config(APP_LABEL)
    clearbit.key = config.clearbit['key']

    # The stream option ensures that the request blocks
    # until Clearbit has found some data on both the person & company.
    response = clearbit.Enrichment.find(email=email, stream=True)

    data = {'email': email}
    if response['person'] is not None:
        data['name'] = response['person']['name']['fullName']
        data['bio'] = response['person'].get('bio', None)
        data['location'] = response['person'].get('location', None)

    if response['company'] is not None:
        data['company'] = response['company']['name']

    return data
