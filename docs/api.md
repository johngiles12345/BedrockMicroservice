# API Documentation

## Overview

The GenAI Bedrock Microservice provides a REST API for generating AI responses using Amazon Bedrock's Claude 3.5 Haiku model.

## Base URL

```
https://{api-gateway-id}.execute-api.us-west-2.amazonaws.com/prod
```

## Authentication

Currently, the API does not require authentication. This may be enhanced in future versions with API keys or OAuth.

## Endpoints

### Generate AI Response

Generate an AI response using the Claude 3.5 Haiku model.

**Endpoint:** `POST /generate`

**Content-Type:** `application/json`

#### Request Body

```json
{
  "prompt": "string"
}
```

**Parameters:**
- `prompt` (string, required): The user input prompt for the AI model
  - Minimum length: 1 character
  - Maximum length: 4000 characters
  - Must be a non-empty string

#### Response

**Success Response (200 OK):**

```json
{
  "message": "Success",
  "response": "AI-generated response text",
  "model_id": "anthropic.claude-3-5-haiku-20241022-v1:0",
  "usage": {
    "input_tokens": 10,
    "output_tokens": 25
  }
}
```

**Error Responses:**

**400 Bad Request:**
```json
{
  "error": "Bad Request",
  "message": "Specific error message"
}
```

Common 400 error messages:
- "Request body is required"
- "Invalid JSON in request body"
- "Missing 'prompt' field in request body"
- "Prompt must be a string"
- "Prompt cannot be empty"
- "Prompt exceeds maximum length of 4000 characters"

**500 Internal Server Error:**
```json
{
  "error": "Internal Server Error",
  "message": "Specific error message"
}
```

Common 500 error messages:
- "Access denied to Bedrock model. Please check IAM permissions."
- "Request throttled. Please try again later."
- "Network or configuration error accessing Bedrock service"
- "Internal server error processing AI request"

## CORS Support

The API supports Cross-Origin Resource Sharing (CORS) with the following headers:

- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: POST, OPTIONS`
- `Access-Control-Allow-Headers: Content-Type, Authorization`

## Rate Limiting

API Gateway provides built-in rate limiting. Default limits:
- 10,000 requests per second
- 5,000 requests per second per API key (if API keys are enabled)

## Examples

### cURL Example

```bash
curl -X POST \
  https://your-api-id.execute-api.us-west-2.amazonaws.com/prod/generate \
  -H 'Content-Type: application/json' \
  -d '{
    "prompt": "Explain the benefits of serverless architecture"
  }'
```

### Python Example

```python
import requests
import json

url = "https://your-api-id.execute-api.us-west-2.amazonaws.com/prod/generate"
headers = {
    "Content-Type": "application/json"
}
data = {
    "prompt": "What are the key principles of cloud-native development?"
}

response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code == 200:
    result = response.json()
    print(f"AI Response: {result['response']}")
    print(f"Tokens used: {result['usage']}")
else:
    print(f"Error: {response.status_code} - {response.text}")
```

### JavaScript Example

```javascript
const apiUrl = 'https://your-api-id.execute-api.us-west-2.amazonaws.com/prod/generate';

const requestData = {
  prompt: 'Describe the advantages of microservices architecture'
};

fetch(apiUrl, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(requestData)
})
.then(response => response.json())
.then(data => {
  if (data.message === 'Success') {
    console.log('AI Response:', data.response);
    console.log('Usage:', data.usage);
  } else {
    console.error('Error:', data.message);
  }
})
.catch(error => {
  console.error('Network error:', error);
});
```

## Error Handling Best Practices

1. **Always check the HTTP status code** before processing the response
2. **Handle network timeouts** gracefully with retry logic
3. **Implement exponential backoff** for rate limiting errors (429)
4. **Log errors appropriately** for debugging and monitoring
5. **Provide user-friendly error messages** in your application

## Monitoring and Logging

All API requests are logged to CloudWatch with the following information:
- Request ID
- Source IP
- HTTP method and path
- Response status code
- Response time
- Request/response size

Use the request ID for troubleshooting specific API calls.
