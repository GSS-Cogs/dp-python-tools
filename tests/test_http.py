import pytest
from unittest import mock
from requests.exceptions import RequestException
from ..dpytools.http_clients.http import HttpClient


@mock.patch('http.requests.get')
def test_get_method(mock_get):
    """
    Test that the get method calls requests.get and 
    returns a response with status code 200
    """
    mock_get.return_value.status_code = 200
    client = HttpClient()
    response = client.get('http://testurl.com')
    assert mock_get.called
    assert response.status_code == 200


@mock.patch('http.requests.post')
def test_post_method(mock_post):
    """
    Test that the post method calls requests.post and
    returns a response with status code 200
    """
    mock_post.return_value.status_code = 200
    client = HttpClient()
    response = client.post('http://testurl.com')
    assert mock_post.called
    assert response.status_code == 200


@mock.patch('http.requests.get')
def test_backoff_on_exception(mock_get):
    """
    Test that the get method retries on RequestException
    """
    mock_get.side_effect = RequestException
    client = HttpClient()
    with pytest.raises(RequestException):
        client.get('http://testurl.com')
    assert mock_get.call_count == client.backoff_max


@mock.patch('http.requests.get')
def test_propagate_kwargs(mock_get):
    """
    Test that the get method propagates keyword arguments
    """
    mock_get.return_value.status_code = 200
    client = HttpClient()
    headers = {'test-header': 'test-value'}
    client.get('http://testurl.com', headers=headers)
    args, kwargs = mock_get.call_args
    assert 'headers' in kwargs
    assert kwargs['headers'] == headers