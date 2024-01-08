import pytest
from unittest.mock import patch, MagicMock
from http.client import HTTPResponse, HTTPException
from dpytools.http_clients.base import BaseHttpClient  

# Mock the HTTPSConnection class
@patch('http.client.HTTPSConnection')
def test_get(mock_connection):
    """
    Test that the get method returns a response object
    """

    # Create a mock response object
    mock_response = MagicMock(HTTPResponse)
    mock_response.status = 200
    mock_response.read.return_value = b'Test response content'
    mock_connection.return_value.getresponse.return_value = mock_response
    
    # Create an instance of BaseHttpClient and make a GET request
    client = BaseHttpClient()
    response = client.get('http://example.com')

    # Assertions to check the response status, content and the connection call
    assert response.status == 200
    assert response.read().decode() == 'Test response content'
    mock_connection.assert_called_once_with('example.com')


@patch('http.client.HTTPSConnection')
def test_post(mock_connection):
    """
    Test that the post method returns a response object
    """

    # Create a mock response object
    mock_response = MagicMock(HTTPResponse)
    mock_response.status = 200
    mock_response.read.return_value = b'Test response content'
    mock_connection.return_value.getresponse.return_value = mock_response
    
    # Create an instance of BaseHttpClient and make a POST request
    client = BaseHttpClient()
    response = client.post('http://example.com')

    # Assertions to check the response status, content and the connection call
    assert response.status == 200
    assert response.read().decode() == 'Test response content'
    mock_connection.assert_called_once_with('example.com')


@patch('http.client.HTTPSConnection')
def test_backoff_on_exception(mock_connection):
    """
    Test that the get method retries on HTTPException
    """

    # Create a mock response object
    mock_response = MagicMock(HTTPResponse)
    mock_response.status = 200

    # Raise HTTPException on the first call, then return the mock_response
    mock_connection.return_value.getresponse.side_effect = [HTTPException('HTTP Error'), mock_response]
    
    # Create an instance of BaseHttpClient and make a GET request
    client = BaseHttpClient()
    response = client.get('http://example.com')

    # Assertions to check the response status and the number of getresponse calls
    assert response.status == 200
    assert mock_connection.return_value.getresponse.call_count == 2


@patch('http.client.HTTPSConnection')
def test_request(mock_connection):
    """
    Test that the _request method returns a response object
    """

    # Create a mock response object
    mock_response = MagicMock(HTTPResponse)
    mock_response.status = 200
    mock_response.read.return_value = b'Test response content'
    mock_connection.return_value.getresponse.return_value = mock_response
    
    # Create an instance of BaseHttpClient and make a request
    client = BaseHttpClient()
    response = client._request('GET', 'http://example.com')

    # Assertions to check the response status, content and the connection call
    assert response.status == 200
    assert response.read().decode() == 'Test response content'
    mock_connection.assert_called_once_with('example.com')


@patch('http.client.HTTPSConnection')
def test_request_with_timeout(mock_connection):
    """
    Test _request method with timeout passed as kwargs
    """

    # Create a mock response object
    mock_response = MagicMock(HTTPResponse)
    mock_response.status = 200
    mock_response.read.return_value = b'Test response content'
    mock_connection.return_value.getresponse.return_value = mock_response
    
    # Create an instance of BaseHttpClient and make a request with a timeout
    client = BaseHttpClient()
    response = client._request('GET', 'http://example.com', timeout=5)

    # Assertions to check the response status, content and the connection call
    assert response.status == 200
    assert response.read().decode() == 'Test response content'
    mock_connection.assert_called_once_with('example.com')