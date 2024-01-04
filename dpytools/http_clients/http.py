import backoff
import requests
import logging


def log_retry(details):
    logging.error(f"Request failed, retrying... Attempt #{details['tries']}")


class HttpClient:
    
    def __init__(self, backoff_max=30):
        self.backoff_max = backoff_max
        
    
    @backoff.on_exception(
            backoff.expo, 
            requests.exceptions.RequestException,
            max_time=lambda self: self.backoff_max,
            on_backoff=log_retry
    )
    def get(self, url, *args, **kwargs):
        # Extract the 'timeout' argument if it exists
        timeout = kwargs.pop('timeout', None) 
        logging.info(f"Sending GET request to {url}")
        return self._request(requests.get, url,timeout=timeout, *args, **kwargs)


    @backoff.on_exception(
            backoff.expo, 
            requests.exceptions.RequestException,
            max_time=lambda self: self.backoff_max,
            on_backoff=log_retry,   
    )
    def post(self, url, *args, **kwargs):
        # Extract the 'timeout' argument if it exists
        timeout = kwargs.pop('timeout', None) 
        logging.info(f"Sending POST request to {url}")
        return self._request(requests.post, url,timeout=timeout, *args, **kwargs)

    
    def _request(self, method, url, *args, **kwargs):
        try:
            response = method(url, *args, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed due to {str(e)}, retrying...")
            raise

    