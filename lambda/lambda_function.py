"""
Lambda function for processing user inputs through Amazon Bedrock Claude 3.5 Haiku model.

This module provides the main Lambda handler function that receives user prompts
via API Gateway, processes them through Amazon Bedrock, and returns the AI-generated
responses.

Author: Development Team
Project: GenAI Bedrock Microservice
"""

import json
import logging
import os
from typing import Dict, Any, Optional

import boto3
from botocore.exceptions import ClientError, BotoCoreError

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize Bedrock client
bedrock_client = boto3.client('bedrock-runtime', region_name=os.environ.get('AWS_DEFAULT_REGION', 'us-west-2'))

# Configuration constants
BEDROCK_MODEL_ID = os.environ.get('BEDROCK_MODEL_ID', 'anthropic.claude-3-5-haiku-20241022-v1:0')
MAX_TOKENS = 4000
TEMPERATURE = 0.7


def create_response(status_code: int, body: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    Create a standardized API Gateway response.
    
    Args:
        status_code: HTTP status code
        body: Response body as dictionary
        headers: Optional HTTP headers
        
    Returns:
        Dict containing the formatted API Gateway response
    """
    default_headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
    }
    
    if headers:
        default_headers.update(headers)
    
    return {
        'statusCode': status_code,
        'headers': default_headers,
        'body': json.dumps(body)
    }


def validate_request(event: Dict[str, Any]) -> Optional[str]:
    """
    Validate the incoming request structure and content.
    
    Args:
        event: Lambda event dictionary
        
    Returns:
        Error message if validation fails, None if valid
    """
    try:
        # Check if body exists
        if 'body' not in event or not event['body']:
            return "Request body is required"
        
        # Parse JSON body
        try:
            body = json.loads(event['body'])
        except json.JSONDecodeError:
            return "Invalid JSON in request body"
        
        # Check if prompt exists and is valid
        if 'prompt' not in body:
            return "Missing 'prompt' field in request body"
        
        prompt = body['prompt']
        if not isinstance(prompt, str):
            return "Prompt must be a string"
        
        if not prompt.strip():
            return "Prompt cannot be empty"
        
        if len(prompt) > 4000:
            return "Prompt exceeds maximum length of 4000 characters"
        
        return None
        
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        return "Invalid request format"


def invoke_bedrock_model(prompt: str) -> Dict[str, Any]:
    """
    Invoke the Bedrock Claude 3.5 Haiku model with the given prompt.
    
    Args:
        prompt: User input prompt
        
    Returns:
        Dictionary containing the model response or error information
        
    Raises:
        ClientError: If there's an AWS service error
        Exception: For other unexpected errors
    """
    try:
        # Prepare the request body for Claude 3.5 Haiku
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        logger.info(f"Invoking Bedrock model: {BEDROCK_MODEL_ID}")
        
        # Invoke the model
        response = bedrock_client.invoke_model(
            modelId=BEDROCK_MODEL_ID,
            body=json.dumps(request_body),
            contentType='application/json',
            accept='application/json'
        )
        
        # Parse the response
        response_body = json.loads(response['body'].read())
        
        # Extract the generated text
        if 'content' in response_body and len(response_body['content']) > 0:
            generated_text = response_body['content'][0]['text']
            
            return {
                'success': True,
                'response': generated_text,
                'model_id': BEDROCK_MODEL_ID,
                'usage': response_body.get('usage', {})
            }
        else:
            logger.error("Unexpected response format from Bedrock")
            return {
                'success': False,
                'error': 'Unexpected response format from AI model'
            }
            
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        logger.error(f"Bedrock ClientError: {error_code} - {error_message}")
        
        if error_code == 'AccessDeniedException':
            return {
                'success': False,
                'error': 'Access denied to Bedrock model. Please check IAM permissions.'
            }
        elif error_code == 'ValidationException':
            return {
                'success': False,
                'error': 'Invalid request to Bedrock model.'
            }
        elif error_code == 'ThrottlingException':
            return {
                'success': False,
                'error': 'Request throttled. Please try again later.'
            }
        else:
            return {
                'success': False,
                'error': f'Bedrock service error: {error_message}'
            }
            
    except BotoCoreError as e:
        logger.error(f"BotoCoreError: {str(e)}")
        return {
            'success': False,
            'error': 'Network or configuration error accessing Bedrock service'
        }
        
    except Exception as e:
        logger.error(f"Unexpected error invoking Bedrock: {str(e)}")
        return {
            'success': False,
            'error': 'Internal server error processing AI request'
        }


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Main Lambda handler function for processing Bedrock requests.
    
    This function serves as the entry point for API Gateway requests, validates
    the input, calls the Bedrock model, and returns the response.
    
    Args:
        event: Lambda event dictionary containing request information
        context: Lambda context object (unused)
        
    Returns:
        Dict containing the API Gateway response
    """
    try:
        logger.info(f"Received event: {json.dumps(event, default=str)}")
        
        # Handle CORS preflight requests
        if event.get('httpMethod') == 'OPTIONS':
            return create_response(200, {'message': 'CORS preflight successful'})
        
        # Validate the request
        validation_error = validate_request(event)
        if validation_error:
            logger.warning(f"Request validation failed: {validation_error}")
            return create_response(400, {
                'error': 'Bad Request',
                'message': validation_error
            })
        
        # Extract the prompt from the request
        body = json.loads(event['body'])
        prompt = body['prompt'].strip()
        
        logger.info(f"Processing prompt of length: {len(prompt)}")
        
        # Invoke the Bedrock model
        bedrock_response = invoke_bedrock_model(prompt)
        
        if bedrock_response['success']:
            logger.info("Successfully generated response from Bedrock")
            return create_response(200, {
                'message': 'Success',
                'response': bedrock_response['response'],
                'model_id': bedrock_response['model_id'],
                'usage': bedrock_response.get('usage', {})
            })
        else:
            logger.error(f"Bedrock invocation failed: {bedrock_response['error']}")
            return create_response(500, {
                'error': 'Internal Server Error',
                'message': bedrock_response['error']
            })
            
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
        return create_response(400, {
            'error': 'Bad Request',
            'message': 'Invalid JSON in request body'
        })
        
    except Exception as e:
        logger.error(f"Unexpected error in lambda_handler: {str(e)}")
        return create_response(500, {
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred'
        })
