"""
Unit tests for the Bedrock Lambda function.

This module contains comprehensive tests for the Lambda function that processes
user inputs through Amazon Bedrock Claude 3.5 Haiku model.

Author: Development Team
Project: GenAI Bedrock Microservice
"""

import json
import pytest
from unittest.mock import Mock, patch, MagicMock
from botocore.exceptions import ClientError, BotoCoreError

# Import the Lambda function module
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lambda'))

from lambda_function import (
    lambda_handler,
    create_response,
    validate_request,
    invoke_bedrock_model
)


class TestCreateResponse:
    """Test cases for the create_response function."""
    
    def test_create_response_basic(self):
        """Test basic response creation."""
        response = create_response(200, {'message': 'success'})
        
        assert response['statusCode'] == 200
        assert 'headers' in response
        assert response['headers']['Content-Type'] == 'application/json'
        assert response['headers']['Access-Control-Allow-Origin'] == '*'
        
        body = json.loads(response['body'])
        assert body['message'] == 'success'
    
    def test_create_response_with_custom_headers(self):
        """Test response creation with custom headers."""
        custom_headers = {'X-Custom-Header': 'test-value'}
        response = create_response(201, {'data': 'test'}, custom_headers)
        
        assert response['statusCode'] == 201
        assert response['headers']['X-Custom-Header'] == 'test-value'
        assert response['headers']['Content-Type'] == 'application/json'


class TestValidateRequest:
    """Test cases for the validate_request function."""
    
    def test_validate_request_valid(self):
        """Test validation with valid request."""
        event = {
            'body': json.dumps({'prompt': 'Hello, how are you?'})
        }
        
        result = validate_request(event)
        assert result is None
    
    def test_validate_request_missing_body(self):
        """Test validation with missing body."""
        event = {}
        
        result = validate_request(event)
        assert result == "Request body is required"
    
    def test_validate_request_empty_body(self):
        """Test validation with empty body."""
        event = {'body': ''}
        
        result = validate_request(event)
        assert result == "Request body is required"
    
    def test_validate_request_invalid_json(self):
        """Test validation with invalid JSON."""
        event = {'body': 'invalid json'}
        
        result = validate_request(event)
        assert result == "Invalid JSON in request body"
    
    def test_validate_request_missing_prompt(self):
        """Test validation with missing prompt field."""
        event = {'body': json.dumps({'message': 'hello'})}
        
        result = validate_request(event)
        assert result == "Missing 'prompt' field in request body"
    
    def test_validate_request_non_string_prompt(self):
        """Test validation with non-string prompt."""
        event = {'body': json.dumps({'prompt': 123})}
        
        result = validate_request(event)
        assert result == "Prompt must be a string"
    
    def test_validate_request_empty_prompt(self):
        """Test validation with empty prompt."""
        event = {'body': json.dumps({'prompt': '   '})}
        
        result = validate_request(event)
        assert result == "Prompt cannot be empty"
    
    def test_validate_request_long_prompt(self):
        """Test validation with overly long prompt."""
        long_prompt = 'a' * 4001
        event = {'body': json.dumps({'prompt': long_prompt})}
        
        result = validate_request(event)
        assert result == "Prompt exceeds maximum length of 4000 characters"


class TestInvokeBedrockModel:
    """Test cases for the invoke_bedrock_model function."""
    
    @patch('lambda_function.bedrock_client')
    def test_invoke_bedrock_model_success(self, mock_bedrock_client):
        """Test successful Bedrock model invocation."""
        # Mock successful response
        mock_response = {
            'body': MagicMock()
        }
        mock_response['body'].read.return_value = json.dumps({
            'content': [{'text': 'Hello! How can I help you today?'}],
            'usage': {'input_tokens': 10, 'output_tokens': 15}
        }).encode('utf-8')
        
        mock_bedrock_client.invoke_model.return_value = mock_response
        
        result = invoke_bedrock_model("Hello")
        
        assert result['success'] is True
        assert result['response'] == 'Hello! How can I help you today?'
        assert 'usage' in result
        assert result['model_id'] == 'anthropic.claude-3-5-haiku-20241022-v1:0'
    
    @patch('lambda_function.bedrock_client')
    def test_invoke_bedrock_model_access_denied(self, mock_bedrock_client):
        """Test Bedrock model invocation with access denied error."""
        mock_bedrock_client.invoke_model.side_effect = ClientError(
            error_response={'Error': {'Code': 'AccessDeniedException', 'Message': 'Access denied'}},
            operation_name='InvokeModel'
        )
        
        result = invoke_bedrock_model("Hello")
        
        assert result['success'] is False
        assert 'Access denied to Bedrock model' in result['error']
    
    @patch('lambda_function.bedrock_client')
    def test_invoke_bedrock_model_throttling(self, mock_bedrock_client):
        """Test Bedrock model invocation with throttling error."""
        mock_bedrock_client.invoke_model.side_effect = ClientError(
            error_response={'Error': {'Code': 'ThrottlingException', 'Message': 'Request throttled'}},
            operation_name='InvokeModel'
        )
        
        result = invoke_bedrock_model("Hello")
        
        assert result['success'] is False
        assert 'Request throttled' in result['error']
    
    @patch('lambda_function.bedrock_client')
    def test_invoke_bedrock_model_validation_error(self, mock_bedrock_client):
        """Test Bedrock model invocation with validation error."""
        mock_bedrock_client.invoke_model.side_effect = ClientError(
            error_response={'Error': {'Code': 'ValidationException', 'Message': 'Invalid request'}},
            operation_name='InvokeModel'
        )
        
        result = invoke_bedrock_model("Hello")
        
        assert result['success'] is False
        assert 'Invalid request to Bedrock model' in result['error']
    
    @patch('lambda_function.bedrock_client')
    def test_invoke_bedrock_model_botocore_error(self, mock_bedrock_client):
        """Test Bedrock model invocation with BotoCoreError."""
        mock_bedrock_client.invoke_model.side_effect = BotoCoreError()
        
        result = invoke_bedrock_model("Hello")
        
        assert result['success'] is False
        assert 'Network or configuration error' in result['error']
    
    @patch('lambda_function.bedrock_client')
    def test_invoke_bedrock_model_unexpected_response_format(self, mock_bedrock_client):
        """Test Bedrock model invocation with unexpected response format."""
        mock_response = {
            'body': MagicMock()
        }
        mock_response['body'].read.return_value = json.dumps({
            'unexpected_field': 'value'
        }).encode('utf-8')
        
        mock_bedrock_client.invoke_model.return_value = mock_response
        
        result = invoke_bedrock_model("Hello")
        
        assert result['success'] is False
        assert 'Unexpected response format' in result['error']


class TestLambdaHandler:
    """Test cases for the main lambda_handler function."""
    
    def test_lambda_handler_options_request(self):
        """Test CORS preflight OPTIONS request."""
        event = {'httpMethod': 'OPTIONS'}
        context = Mock()
        
        response = lambda_handler(event, context)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['message'] == 'CORS preflight successful'
    
    def test_lambda_handler_invalid_request(self):
        """Test handler with invalid request."""
        event = {'body': 'invalid json'}
        context = Mock()
        
        response = lambda_handler(event, context)
        
        assert response['statusCode'] == 400
        body = json.loads(response['body'])
        assert body['error'] == 'Bad Request'
    
    @patch('lambda_function.invoke_bedrock_model')
    def test_lambda_handler_success(self, mock_invoke_bedrock):
        """Test successful request processing."""
        # Mock successful Bedrock response
        mock_invoke_bedrock.return_value = {
            'success': True,
            'response': 'Hello! How can I help you?',
            'model_id': 'anthropic.claude-3-5-haiku-20241022-v1:0',
            'usage': {'input_tokens': 5, 'output_tokens': 10}
        }
        
        event = {
            'httpMethod': 'POST',
            'body': json.dumps({'prompt': 'Hello'})
        }
        context = Mock()
        
        response = lambda_handler(event, context)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['message'] == 'Success'
        assert body['response'] == 'Hello! How can I help you?'
        assert 'usage' in body
    
    @patch('lambda_function.invoke_bedrock_model')
    def test_lambda_handler_bedrock_failure(self, mock_invoke_bedrock):
        """Test handler when Bedrock invocation fails."""
        # Mock failed Bedrock response
        mock_invoke_bedrock.return_value = {
            'success': False,
            'error': 'Access denied to Bedrock model'
        }
        
        event = {
            'httpMethod': 'POST',
            'body': json.dumps({'prompt': 'Hello'})
        }
        context = Mock()
        
        response = lambda_handler(event, context)
        
        assert response['statusCode'] == 500
        body = json.loads(response['body'])
        assert body['error'] == 'Internal Server Error'
        assert 'Access denied' in body['message']
    
    def test_lambda_handler_json_decode_error(self):
        """Test handler with JSON decode error in main function."""
        event = {
            'httpMethod': 'POST',
            'body': '{"prompt": "Hello"'  # Invalid JSON - missing closing brace
        }
        context = Mock()
        
        response = lambda_handler(event, context)
        
        assert response['statusCode'] == 400
        body = json.loads(response['body'])
        assert body['error'] == 'Bad Request'
        assert 'Invalid JSON' in body['message']


if __name__ == '__main__':
    pytest.main([__file__])
