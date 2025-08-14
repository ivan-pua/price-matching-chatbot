# import boto3
# import os
# import json
# from botocore.config import Config

# # Set your API key as environment variable
# os.environ['AWS_BEARER_TOKEN_BEDROCK'] = "your_actual_api_key_here"  # Replace with your actual key

# # Use 'bedrock-agent' service with correct region code
# bedrock_agent = boto3.client(
#     service_name='bedrock-agent',
#     region_name='us-west-2',
#     config=Config(
#         signature_version='v4',
#         retries={'max_attempts': 3, 'mode': 'standard'}
#     )
# )

# try:
#     response = bedrock_agent.get_prompt(
#         promptIdentifier='arn:aws:bedrock:us-west-2:974000698068:prompt/S8TPWVPSX3'
#     )
    
#     # Print the entire response object
#     print("=== FULL RESPONSE ===")
#     print(json.dumps(response, indent=2, default=str))
    
#     print("\n=== AVAILABLE KEYS ===")
#     print(f"Response keys: {list(response.keys())}")
    
#     # Safe access to common fields
#     print(f"\n=== BASIC INFO ===")
#     print(f"Prompt Name: {response.get('name', 'N/A')}")
#     print(f"Prompt ARN: {response.get('arn', 'N/A')}")
#     print(f"Prompt ID: {response.get('id', 'N/A')}")
#     print(f"Version: {response.get('version', 'N/A')}")
#     print(f"Created At: {response.get('createdAt', 'N/A')}")
#     print(f"Updated At: {response.get('updatedAt', 'N/A')}")
    
#     # Check for variants (where the actual prompt content usually is)
#     if 'variants' in response:
#         print(f"\n=== VARIANTS ===")
#         for i, variant in enumerate(response['variants']):
#             print(f"Variant {i+1}:")
#             print(f"  Name: {variant.get('name', 'N/A')}")
#             print(f"  Model ID: {variant.get('modelId', 'N/A')}")
            
#             # Check for template configuration
#             if 'templateConfiguration' in variant:
#                 template_config = variant['templateConfiguration']
#                 print(f"  Template Type: {template_config.get('templateType', 'N/A')}")
                
#                 # Check for text template
#                 if 'text' in template_config:
#                     text_template = template_config['text']
#                     print(f"  Template Text: {text_template.get('text', 'N/A')}")
                    
#                     # Input variables
#                     if 'inputVariables' in text_template:
#                         print(f"  Input Variables: {text_template['inputVariables']}")
    
# except Exception as e:
#     print(f"Error retrieving prompt: {str(e)}")

import boto3
import os
import json
from botocore.config import Config

# Set your API key as environment variable
os.environ['AWS_BEARER_TOKEN_BEDROCK'] = "bedrock-api-key-YmVkcm9jay5hbWF6b25hd3MuY29tLz9BY3Rpb249Q2FsbFdpdGhCZWFyZXJUb2tlbiZYLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFTSUE2RlJYWEdMS09FRzVZRkkyJTJGMjAyNTA4MTQlMkZ1cy13ZXN0LTIlMkZiZWRyb2NrJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNTA4MTRUMDExMzIzWiZYLUFtei1FeHBpcmVzPTQzMjAwJlgtQW16LVNlY3VyaXR5LVRva2VuPUlRb0piM0pwWjJsdVgyVmpFUEglMkYlMkYlMkYlMkYlMkYlMkYlMkYlMkYlMkYlMkZ3RWFDWFZ6TFhkbGMzUXRNaUpHTUVRQ0lGWCUyQmtXOVRMbEVjbFkyZiUyQmd3dG91bHNnbGFFYlFDZTBIbVR6UU92d2RJaEFpQU9DRWZ3WnBQYjI4WmJCNmQ5Y0VaWnpjVUlURnAzaFEyQlVZJTJCVHhPeW5yeXEwQXdnNkVBSWFERGszTkRBd01EWTVPREEyT0NJTXE3cDZFaDlUQ3hidTRrWkdLcEVER000UGxpVmJiWHFzNmpSNndza0RjZ1FyWWd1UGdxY0hRelFMQ1Exdk5RZWhRTThNY3hJMFl3bTBFVmh0UEJMVG9tWmNZaEs5UVBiamtJJTJGUWRIQ3lZTVZDSW9XMUpjJTJGV2NMUHclMkJIYUUlMkIyJTJCTjl6MiUyRjJnSHV4dGglMkZXNk9mZ1FsS0h3dzA0c2VqRUNlYnBRWTU2d2x5eHc0RGp5THdnRzFOTFlHR3c5b0wlMkY5VU9VaEZZbmplbFIxSTZXNU02RlM0eG8yN1daYjF1eUtLTkZJS0VrNnR0cUdsakhHeFRIcWhBT1FRenY4ZWpBaEtKUkdldzZvWXczTSUyQnlKNlNLdEFuNlVicFR4TVFraG1MdThmJTJGeG42SVZqQUdxViUyQmlLUkF0ZSUyRnNldHVYbVBzU1hJZnNKMG5hcGZKa3pvaVJJSFg3bTFDeUlBMk02Y2IlMkZUR2VHWFUlMkZnNWJPNFNZaUNjc21wNkZUJTJGcUE1bk40UTRYM0NWMXIzTTdoZDR5VGF3JTJCTjUlMkZkNlQzd2gwcmp4TXMlMkJuMlJvcDkyQ1Q1R0pGUFRsbEJ2WndETG4xc1RqZXVsdTBndU50QXV1QjRUTjZOM0l0Tm1GcVd2cmlWNWRuSGNaUnNhQTkxU3BmZFZWNFJsRnE4JTJGeXZRWjU5VzRkMSUyRm5hJTJGdE1QSWhPZCUyQkJicWQ5eWNkZ05RaldKdXFXMVZlNE1vZkF1JTJCZzJ4RlFTM2N3NGNuMHhBWTZ1QUxqZW5EamJ6Q2RqZkRaaGF0U0hsRXZkbnZsYmpQSE5mZ3QlMkZ0TjBFJTJCZ0pjc0R6U3VHVU1IaXpzQVNlYVFkd3RQQUh4Y1lQS3VEUGZuWFlpNjhMRzhuSWJjSDdzUlFPaFlFQmdwWGJkRVVyWTlidkhGTGF1TE1xdWkzclN2Y1BCVWlrJTJCYTBqY2FTUnVscUJzJTJCZTB6UGtSazU0N3ZPMHo1NHdGdXFVTG5FZjdla3hObE5pZTRkaE5iNzJ1SSUyRlNPWUtvMTN4TVp0SXYzZnZXYU5FV002Sk0lMkI2cElWYiUyRjBtTG1ERDFMYm9LcUxVc2tIRDRPZEF6M1g0VnRKUXBxbDBKQkFGcGg0azRaMHpKa3YwaEZRNXJJWnFWeDRiNTRKdm8xVmhGeTZvbm13MHNuanNSRjJEdVA4QW9BYyUyRmdMSWhQZzFpYnJrYnV2RHhmY1Z1ZzVhNDNpTE5XOGIxSTJpSFNwT3FQQ1lYVmYlMkJVOUNQVXRqTkVseHVtQ1hUVUZTbDdQYWFHWXZKc3MxaiUyRmxaM0poTWFveDJNS2owOXFuM1NpTFlzJTNEJlgtQW16LVNpZ25hdHVyZT1hZDA1Y2QxYzAzNDNkN2QxMjFiNzhlZjg2MjEwMGI1YTIxOTVjMTBjZGY2ZDBiY2Y4NmU2NWI4YjgwODNhYjJkJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZWZXJzaW9uPTE="  # Replace with your actual key

# Create both clients - one for prompt management, one for runtime
bedrock_agent = boto3.client(
    service_name='bedrock-agent',
    region_name='us-west-2',
    config=Config(
        signature_version='v4',
        retries={'max_attempts': 3, 'mode': 'standard'}
    )
)

bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-west-2',
    config=Config(
        signature_version='v4',
        retries={'max_attempts': 3, 'mode': 'standard'}
    )
)

try:
    # First, get the prompt details
    prompt_response = bedrock_agent.get_prompt(
        promptIdentifier='arn:aws:bedrock:us-west-2:974000698068:prompt/S8TPWVPSX3'
    )
    
    print(f"Retrieved prompt: {prompt_response['name']}")
    
    # Now invoke the prompt with your input
    invoke_response = bedrock_runtime.invoke_model(
        modelId='us.anthropic.claude-sonnet-4-20250514-v1:0',  # Adjust model ID as needed
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": "Compare telco plans for unlimited data under $60 in Australia"  # Your query here
                }
            ]
        })
    )
    
    # Parse the response
    response_body = json.loads(invoke_response['body'].read())
    
    print("\n=== PROMPT RESPONSE ===")
    print(response_body['content'][0]['text'])
    
    # Now you can send a follow-up question
    follow_up_response = bedrock_runtime.invoke_model(
        modelId='anthropic.claude-3-sonnet-20240229-v1:0',
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": "Compare telco plans for unlimited data under $60 in Australia"
                },
                {
                    "role": "assistant", 
                    "content": response_body['content'][0]['text']
                },
                {
                    "role": "user",
                    "content": "Which of these plans has the best international roaming options?"  # Follow-up question
                }
            ]
        })
    )
    
    follow_up_body = json.loads(follow_up_response['body'].read())
    
    print("\n=== FOLLOW-UP RESPONSE ===")
    print(follow_up_body['content'][0]['text'])
    
except Exception as e:
    print(f"Error: {str(e)}")
