import backoff
import http.client
from http.client import HTTPException
from urllib.parse import urlparse
import logging


# Function to log retry attempts
def log_retry(details):
    logging.error(f"Request failed, retrying... Attempt #{details['tries']}")


class HttpClient:
    # Initialize HttpClient with a backoff_max value
    def __init__(self, backoff_max=30):
        self.backoff_max = backoff_max

    # GET request method with exponential backoff
    @backoff.on_exception(
        backoff.expo, 
        HTTPException,
        max_time=30,  
        on_backoff=log_retry
    )
    def get(self, url, *args, **kwargs):
        timeout = kwargs.pop('timeout', None)
        logging.info(f"Sending GET request to {url}")
        return self._request("GET", url, timeout=timeout, *args, **kwargs)

    # POST request method with exponential backoff
    @backoff.on_exception(
        backoff.expo, 
        HTTPException,
        max_time=30, 
        on_backoff=log_retry,
    )
    def post(self, url, *args, **kwargs):
        timeout = kwargs.pop('timeout', None)
        logging.info(f"Sending POST request to {url}")
        return self._request("POST", url, timeout=timeout, *args, **kwargs)

    # Private method to handle the request
    def _request(self, method, url, *args, **kwargs):
        try:
            headers = kwargs.pop('headers', {})

            url_parts = urlparse(url)
            https_connection = http.client.HTTPSConnection(url_parts.netloc)
            path = url_parts.path or '/'
            https_connection.request(method, path, headers=headers, *args, **kwargs)
            
            response = https_connection.getresponse()
            response_content = response.read()
            https_connection.close() 

            # Raise an exception if the HTTP status is 400 or above
            if response.status >= 400:
                raise HTTPException(f"HTTP request failed with status {response.status}, response: {response_content.decode()}")

            return response

        # Handle HTTPException separately to log and retry
        except HTTPException as e:
            logging.error(f"Request failed due to {str(e)}, retrying...")
            raise
        # Handle other exceptions
        except Exception as e:
            logging.error(f"An unexpected error occurred: {str(e)}")
            raise