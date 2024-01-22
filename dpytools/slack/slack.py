import os
import logging
from dpytools.http_clients.base import BaseHttpClient

class SlackNotifier:

    def __init__(self):
        self.webhook_url = os.getenv("SLACK_WEBHOOK_URL")
        if not self.webhook_url:
            raise ValueError('SLACK_WEBHOOK_URL is not set')
        self.http_client = BaseHttpClient()
        self.validate_webhook_url()

    def validate_webhook_url(self):
        response = self.http_client.get(self.webhook_url)
        if response.status_code != 200:
            logging.error(f'Invalid SLACK_WEBHOOK_URL: {response.status_code}')
            raise ValueError('Invalid SLACK_WEBHOOK_URL')

    def notify(self, msg: dict):
        try:
            response = self.http_client.post(self.webhook_url, json=msg)
            response.raise_for_status()
        except Exception as e:
            logging.error(f'Failed to send notification: {e}')
