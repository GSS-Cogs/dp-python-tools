import pytest
from unittest.mock import patch, MagicMock
from requests import HTTPError, Response
from dpytools.http_clients.base import BaseHttpClient
from dpytools.slack.slack import SlackNotifier

@patch('os.getenv')
@patch.object(BaseHttpClient, 'get')
def test_validate_webhook_url(mock_get, mock_getenv):
    """
    Test that the validate_webhook_url method raises an exception for invalid URLs
    """
    mock_getenv.return_value = 'http://example.com'
    mock_response = MagicMock(Response)
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    with pytest.raises(ValueError):
        notifier = SlackNotifier()

@patch('os.getenv')
@patch.object(BaseHttpClient, 'get')
def test_validate_webhook_url_success(mock_get, mock_getenv):
    """
    Test that the validate_webhook_url method does not raise an exception for valid URLs
    """
    mock_getenv.return_value = 'http://example.com'
    mock_response = MagicMock(Response)
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    try:
        notifier = SlackNotifier()
    except ValueError:
        pytest.fail("Unexpected ValueError ..")

@patch('os.getenv')
@patch.object(BaseHttpClient, 'post')
def test_notify(mock_post, mock_getenv):
    """
    Test that the notify method sends a POST request
    """
    mock_getenv.return_value = 'http://example.com'
    mock_response = MagicMock(Response)
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    notifier = SlackNotifier()
    notifier.notify({'text': 'Test message'})

    mock_post.assert_called_once_with('http://example.com', json={'text': 'Test message'})