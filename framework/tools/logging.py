import json

import curlify
import allure
from allure_commons.types import AttachmentType
from requests import Response


def log_request(response: Response) -> None:
    """Logging request and response data to Allure report"""

    method, url = response.request.method, response.request.url

    with allure.step(f"{method} {url}"):
        message = curlify.to_curl(response.request)
        allure.attach(
            body=message.encode("utf8"),
            name=f"Request {method} {response.status_code}",
            attachment_type=allure.attachment_type.TEXT,
            extension="txt",
        )

        if (
            "application/json" in response.headers.get("Content-Type", "")
            and response.text
        ):
            try:
                body = response.json()
                allure.attach(
                    body=json.dumps(body, indent=2),
                    name="Response body",
                    attachment_type=AttachmentType.JSON,
                )
            except json.decoder.JSONDecodeError:
                allure.attach(
                    body=response.text,
                    name="Non-JSON Response body",
                    attachment_type=allure.attachment_type.TEXT,
                )
        else:
            allure.attach(
                body=response.text,
                name="Non-JSON Response body",
                attachment_type=allure.attachment_type.TEXT,
            )
