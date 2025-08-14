import boto3
import os
import json
from botocore.config import Config

# Set your API key as environment variable
os.environ['AWS_BEARER_TOKEN_BEDROCK'] = "your_actual_api_key_here"  # Replace with your actual key

# Use 'bedrock-agent' service with correct region code
bedrock_agent = boto3.client(
    service_name='bedrock-agent',
    region_name='us-west-2',
    config=Config(
        signature_version='v4',
        retries={'max_attempts': 3, 'mode': 'standard'}
    )
)

try:
    response = bedrock_agent.get_prompt(
        promptIdentifier='arn:aws:bedrock:us-west-2:974000698068:prompt/S8TPWVPSX3'
    )
    
    # Print the entire response object
    print("=== FULL RESPONSE ===")
    print(json.dumps(response, indent=2, default=str))
    
    print("\n=== AVAILABLE KEYS ===")
    print(f"Response keys: {list(response.keys())}")
    
    # Safe access to common fields
    print(f"\n=== BASIC INFO ===")
    print(f"Prompt Name: {response.get('name', 'N/A')}")
    print(f"Prompt ARN: {response.get('arn', 'N/A')}")
    print(f"Prompt ID: {response.get('id', 'N/A')}")
    print(f"Version: {response.get('version', 'N/A')}")
    print(f"Created At: {response.get('createdAt', 'N/A')}")
    print(f"Updated At: {response.get('updatedAt', 'N/A')}")
    
    # Check for variants (where the actual prompt content usually is)
    if 'variants' in response:
        print(f"\n=== VARIANTS ===")
        for i, variant in enumerate(response['variants']):
            print(f"Variant {i+1}:")
            print(f"  Name: {variant.get('name', 'N/A')}")
            print(f"  Model ID: {variant.get('modelId', 'N/A')}")
            
            # Check for template configuration
            if 'templateConfiguration' in variant:
                template_config = variant['templateConfiguration']
                print(f"  Template Type: {template_config.get('templateType', 'N/A')}")
                
                # Check for text template
                if 'text' in template_config:
                    text_template = template_config['text']
                    print(f"  Template Text: {text_template.get('text', 'N/A')}")
                    
                    # Input variables
                    if 'inputVariables' in text_template:
                        print(f"  Input Variables: {text_template['inputVariables']}")
    
except Exception as e:
    print(f"Error retrieving prompt: {str(e)}")
