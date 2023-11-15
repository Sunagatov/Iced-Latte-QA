import json

import curlify
import allure
from allure_commons.types import AttachmentType


def log_request(response):
    method, url, body = response.request.method, response.request.url, response.json()

    with allure.step(f'{method} {url}'):
        message = curlify.to_curl(response.request)
        # logging.info(f'{response.status_code} {message}')
        allure.attach(
                body=message.encode('utf8'),
                name=f'Request {method} {response.status_code}',
                attachment_type=allure.attachment_type.TEXT,
                extension='txt'
        )
        allure.attach(
            body=json.dumps(body, indent=2),
            name='Response body',
            attachment_type=AttachmentType.JSON
        )
