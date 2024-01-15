import backoff
import requests
from requests.exceptions import HTTPError
import logging


# Function to log retry attempts
def log_retry(details):
    logging.error(f"Request failed, retrying... Attempt #{details['tries']}")


class BaseHttpClient:
    # Initialize HttpClient with a backoff_max value
    def __init__(self, backoff_max=30):
        self.backoff_max = backoff_max

    # GET request method with exponential backoff
    @backoff.on_exception(backoff.expo, HTTPError, max_time=30, on_backoff=log_retry)
    def get(self, url, *args, **kwargs):
        return self._handle_request("GET", url, *args, **kwargs)

    # POST request method with exponential backoff
    @backoff.on_exception(
        backoff.expo,
        HTTPError,
        max_time=30,
        on_backoff=log_retry,
    )
    def post(self, url, *args, **kwargs):
        return self._handle_request("POST", url, *args, **kwargs)

    # Method to handle requests for GET and POST
    def _handle_request(self, method, url, *args, **kwargs):
        timeout = kwargs.pop("timeout", None)
        logging.info(f"Sending {method} request to {url}")
        try:
            response = requests.request(method, url, timeout=timeout, *args, **kwargs)
            response.raise_for_status()
            return response

        except HTTPError as http_err:
            logging.error(
                f"HTTP error occurred: {http_err} when sending a {method} to {url} with headers {kwargs.get('headers')}"
            )
            raise
        except Exception as err:
            logging.error(
                f"Other error occurred: {err} when sending a {method} to {url} with headers {kwargs.get('headers')}"
            )
            raise
