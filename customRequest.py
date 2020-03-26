import os
from requests import Request, Session, hooks
from twilio.http.http_client import TwilioHttpClient
from twilio.http.response import Response

class MyRequestClass(TwilioHttpClient):
    def __init__(self):
        self.response = None

    def request(self, method, url, params=None, data=None, headers=None, files=None, auth=None, timeout=None,
                allow_redirects=False):
        # Here you can change the URL, headers and other request parameters
        kwargs = {
            'method': method.upper(),
            'url': url,
            'params': params,
            'data': data,
            'headers': headers,
            'files': files,
            'auth': auth,
        }

        session = Session()
        request = Request(**kwargs)

        prepped_request = session.prepare_request(request)

        response = session.send(
            prepped_request,
            allow_redirects=allow_redirects,
            timeout=timeout,
        )

        return Response(int(response.status_code), response.text)