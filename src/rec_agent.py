import boto3
import json
import os
from botocore.config import Config



# Mock conversation data in free text format
MOCK_CONVERSATION_1 = """
SESSION: telco-prompt-session-customer001
CUSTOMER: customer001
TIMESTAMP: 2025-08-13 17:20:05

USER: Hi, I need a cheap mobile plan with decent data. My budget is around $30-40 per month.

AGENT: Based on your budget of $30-40, I recommend these excellent options:

**1. Boost Mobile - $30/month**
- 20GB data (with rollover)
- Unlimited calls & texts
- Uses Telstra network
- No lock-in contract

**2. Woolworths Mobile - $35/month**
- 25GB data
- Unlimited calls & texts
- Uses Telstra network
- 10% off groceries with Everyday Rewards

**3. Aldi Mobile - $35/month**
- 26GB data
- Unlimited calls & texts
- Uses Telstra network
- Great value for money

All these plans offer excellent coverage and value within your budget. Would you like more details about any specific plan?

USER: The Woolworths one sounds interesting. Can you tell me more about the grocery discount?

AGENT: Great choice! Here are the details about Woolworths Mobile benefits:

**Woolworths Mobile $35 Plan Benefits:**
- 25GB monthly data allowance
- Unlimited national calls & SMS
- Uses Telstra 4G network (excellent coverage)
- **10% off groceries** when you spend $50+ at Woolworths
- **10% off mobile plan** when you spend $50+ at Woolworths
- No lock-in contract
- International calls to 35+ countries included

**Additional perks:**
- Free voicemail
- Call waiting & caller ID
- Tethering included
- Unused data expires monthly (no rollover)

The grocery discount alone could save you $5-10 per week if you're a regular Woolworths shopper. Would you like me to help you sign up or compare with other options?

USER: Perfect! How do I sign up for this plan?

AGENT: Excellent! Here's how to sign up for Woolworths Mobile:

**Sign-up Process:**
1. **Online**: Visit woolworthsmobile.com.au
2. **In-store**: Visit any Woolworths supermarket
3. **Phone**: Call 1300 10 1234

**What you'll need:**
- Photo ID (driver's license or passport)
- Proof of address (utility bill or bank statement)
- Credit/debit card for payment
- Your current phone number (if keeping it)

**Steps:**
1. Choose your plan ($35/month - 25GB)
2. Select a new number or port your existing one
3. Choose SIM delivery (free) or collect in-store
4. Set up automatic payments

**Activation:** Usually takes 2-4 hours for new numbers, or up to 24 hours for number porting.

Would you like me to help you with anything else about this plan or compare it with alternatives?
"""




# Set your API key
os.environ['AWS_BEARER_TOKEN_BEDROCK'] = "bedrock-api-key-YmVkcm9jay5hbWF6b25hd3MuY29tLz9BY3Rpb249Q2FsbFdpdGhCZWFyZXJUb2tlbiZYLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFTSUE2RlJYWEdMS09FRzVZRkkyJTJGMjAyNTA4MTQlMkZ1cy13ZXN0LTIlMkZiZWRyb2NrJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNTA4MTRUMDExMzIzWiZYLUFtei1FeHBpcmVzPTQzMjAwJlgtQW16LVNlY3VyaXR5LVRva2VuPUlRb0piM0pwWjJsdVgyVmpFUEglMkYlMkYlMkYlMkYlMkYlMkYlMkYlMkYlMkYlMkZ3RWFDWFZ6TFhkbGMzUXRNaUpHTUVRQ0lGWCUyQmtXOVRMbEVjbFkyZiUyQmd3dG91bHNnbGFFYlFDZTBIbVR6UU92d2RJaEFpQU9DRWZ3WnBQYjI4WmJCNmQ5Y0VaWnpjVUlURnAzaFEyQlVZJTJCVHhPeW5yeXEwQXdnNkVBSWFERGszTkRBd01EWTVPREEyT0NJTXE3cDZFaDlUQ3hidTRrWkdLcEVER000UGxpVmJiWHFzNmpSNndza0RjZ1FyWWd1UGdxY0hRelFMQ1Exdk5RZWhRTThNY3hJMFl3bTBFVmh0UEJMVG9tWmNZaEs5UVBiamtJJTJGUWRIQ3lZTVZDSW9XMUpjJTJGV2NMUHclMkJIYUUlMkIyJTJCTjl6MiUyRjJnSHV4dGglMkZXNk9mZ1FsS0h3dzA0c2VqRUNlYnBRWTU2d2x5eHc0RGp5THdnRzFOTFlHR3c5b0wlMkY5VU9VaEZZbmplbFIxSTZXNU02RlM0eG8yN1daYjF1eUtLTkZJS0VrNnR0cUdsakhHeFRIcWhBT1FRenY4ZWpBaEtKUkdldzZvWXczTSUyQnlKNlNLdEFuNlVicFR4TVFraG1MdThmJTJGeG42SVZqQUdxViUyQmlLUkF0ZSUyRnNldHVYbVBzU1hJZnNKMG5hcGZKa3pvaVJJSFg3bTFDeUlBMk02Y2IlMkZUR2VHWFUlMkZnNWJPNFNZaUNjc21wNkZUJTJGcUE1bk40UTRYM0NWMXIzTTdoZDR5VGF3JTJCTjUlMkZkNlQzd2gwcmp4TXMlMkJuMlJvcDkyQ1Q1R0pGUFRsbEJ2WndETG4xc1RqZXVsdTBndU50QXV1QjRUTjZOM0l0Tm1GcVd2cmlWNWRuSGNaUnNhQTkxU3BmZFZWNFJsRnE4JTJGeXZRWjU5VzRkMSUyRm5hJTJGdE1QSWhPZCUyQkJicWQ5eWNkZ05RaldKdXFXMVZlNE1vZkF1JTJCZzJ4RlFTM2N3NGNuMHhBWTZ1QUxqZW5EamJ6Q2RqZkRaaGF0U0hsRXZkbnZsYmpQSE5mZ3QlMkZ0TjBFJTJCZ0pjc0R6U3VHVU1IaXpzQVNlYVFkd3RQQUh4Y1lQS3VEUGZuWFlpNjhMRzhuSWJjSDdzUlFPaFlFQmdwWGJkRVVyWTlidkhGTGF1TE1xdWkzclN2Y1BCVWlrJTJCYTBqY2FTUnVscUJzJTJCZTB6UGtSazU0N3ZPMHo1NHdGdXFVTG5FZjdla3hObE5pZTRkaE5iNzJ1SSUyRlNPWUtvMTN4TVp0SXYzZnZXYU5FV002Sk0lMkI2cElWYiUyRjBtTG1ERDFMYm9LcUxVc2tIRDRPZEF6M1g0VnRKUXBxbDBKQkFGcGg0azRaMHpKa3YwaEZRNXJJWnFWeDRiNTRKdm8xVmhGeTZvbm13MHNuanNSRjJEdVA4QW9BYyUyRmdMSWhQZzFpYnJrYnV2RHhmY1Z1ZzVhNDNpTE5XOGIxSTJpSFNwT3FQQ1lYVmYlMkJVOUNQVXRqTkVseHVtQ1hUVUZTbDdQYWFHWXZKc3MxaiUyRmxaM0poTWFveDJNS2owOXFuM1NpTFlzJTNEJlgtQW16LVNpZ25hdHVyZT1hZDA1Y2QxYzAzNDNkN2QxMjFiNzhlZjg2MjEwMGI1YTIxOTVjMTBjZGY2ZDBiY2Y4NmU2NWI4YjgwODNhYjJkJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZWZXJzaW9uPTE="

class TelcoPromptConversationAgent:
    def __init__(self):
        self.prompt_arn = "arn:aws:bedrock:us-west-2:974000698068:prompt/S8TPWVPSX3"
        
        # Initialize clients
        self.bedrock_agent = boto3.client(
            service_name='bedrock-agent',
            region_name='us-west-2',
            config=Config(signature_version='v4', retries={'max_attempts': 3, 'mode': 'standard'})
        )
        
        self.bedrock_agent_runtime = boto3.client(
            service_name='bedrock-agent-runtime',
            region_name='us-west-2',
            config=Config(signature_version='v4', retries={'max_attempts': 3, 'mode': 'standard'})
        )
        
        self.bedrock_runtime = boto3.client(
            service_name='bedrock-runtime',
            region_name='us-west-2',
            config=Config(signature_version='v4', retries={'max_attempts': 3, 'mode': 'standard'})
        )
        
        self.prompt_data = None
        self.agent_id = None
        self.conversations = {}
    
    def load_prompt_data(self):
        """Load the prompt data from your ARN"""
        try:
            response = self.bedrock_agent.get_prompt(
                promptIdentifier=self.prompt_arn
            )
            self.prompt_data = response
            print(f"✅ Loaded prompt: {response['name']}")
            print(f"   ARN: {response['arn']}")
            print(f"   Created: {response.get('createdAt', 'N/A')}")
            return True
        except Exception as e:
            print(f"❌ Error loading prompt: {str(e)}")
            return False
    
    def create_agent_from_prompt(self):
        """Create a Bedrock Agent that uses your prompt's knowledge"""
        if not self.prompt_data:
            print("❌ Prompt data not loaded. Call load_prompt_data() first.")
            return False
        
        try:
            # Extract prompt instructions from your prompt
            prompt_instructions = self.extract_prompt_instructions()
            
            agent_response = self.bedrock_agent.create_agent(
                agentName='TelcoPromptConversationAgent',
                description=f'Agent created from prompt: {self.prompt_data["name"]}',
                foundationModel='us.anthropic.claude-sonnet-4-20250514-v1:0',
                instruction=f"""You are a telco customer service agent based on the telco_chatbot prompt.
                
{prompt_instructions}

Your role is to:
1. Help customers find suitable mobile plans
2. Compare different telco options
3. Provide pricing and feature information
4. Answer questions about data, calls, and messaging
5. Assist with plan recommendations based on usage patterns

Always be helpful, accurate, and customer-focused.""",
                
                idleSessionTTLInSeconds=1800,
                # Note: You'll need to create this IAM role first
                agentResourceRoleArn='arn:aws:iam::974000698068:role/AmazonBedrockExecutionRoleForAgents_TelcoAgent'
            )
            
            self.agent_id = agent_response['agent']['agentId']
            print(f"✅ Agent created successfully!")
            print(f"   Agent ID: {self.agent_id}")
            print(f"   Agent ARN: {agent_response['agent']['agentArn']}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating agent: {str(e)}")
            return False
    
    def extract_prompt_instructions(self):
        """Extract instructions from your prompt template"""
        try:
            if 'variants' in self.prompt_data:
                for variant in self.prompt_data['variants']:
                    if 'templateConfiguration' in variant:
                        template_config = variant['templateConfiguration']
                        if 'text' in template_config:
                            return template_config['text'].get('text', 'No template text found')
            return "Use telco knowledge to help customers with mobile plan recommendations."
        except Exception as e:
            print(f"Warning: Could not extract prompt instructions: {str(e)}")
            return "Use telco knowledge to help customers with mobile plan recommendations."
    
    def start_conversation_from_prompt(self, customer_id, initial_message):
        """Start a new conversation using the agent created from your prompt"""
        if not self.agent_id:
            print("❌ Agent not created. Call create_agent_from_prompt() first.")
            return None, None
        
        session_id = f"telco-prompt-session-{customer_id}"
        
        try:
            response = self.bedrock_agent_runtime.invoke_agent(
                agentId=self.agent_id,
                agentAliasId='TSTALIASID',  # Default test alias
                sessionId=session_id,
                inputText=initial_message
            )
            
            # Process the streaming response
            agent_response = self._process_agent_response(response)
            
            # Store conversation
            self.conversations[session_id] = {
                'customer_id': customer_id,
                'messages': [
                    {'role': 'user', 'content': initial_message, 'timestamp': self._get_timestamp()},
                    {'role': 'agent', 'content': agent_response, 'timestamp': self._get_timestamp()}
                ],
                'prompt_arn': self.prompt_arn,
                'agent_id': self.agent_id
            }
            
            return agent_response, session_id
            
        except Exception as e:
            print(f"❌ Error starting conversation: {str(e)}")
            return None, None
    
    def continue_prompt_conversation(self, session_id, user_message):
        """Continue an existing conversation from your prompt"""
        if session_id not in self.conversations:
            return "❌ Session not found. Please start a new conversation."
        
        try:
            response = self.bedrock_agent_runtime.invoke_agent(
                agentId=self.agent_id,
                agentAliasId='TSTALIASID',
                sessionId=session_id,
                inputText=user_message
            )
            
            agent_response = self._process_agent_response(response)
            
            # Update conversation history
            self.conversations[session_id]['messages'].extend([
                {'role': 'user', 'content': user_message, 'timestamp': self._get_timestamp()},
                {'role': 'agent', 'content': agent_response, 'timestamp': self._get_timestamp()}
            ])
            
            return agent_response
            
        except Exception as e:
            print(f"❌ Error continuing conversation: {str(e)}")
            return f"Error: {str(e)}"
    
    def get_prompt_conversation_history(self, session_id):
        """Get the full conversation history for a session"""
        if session_id in self.conversations:
            return self.conversations[session_id]
        return None
    
    def list_prompt_conversations(self):
        """List all conversations created from your prompt"""
        return {
            session_id: {
                'customer_id': conv['customer_id'],
                'message_count': len(conv['messages']),
                'last_message': conv['messages'][-1]['timestamp'] if conv['messages'] else None
            }
            for session_id, conv in self.conversations.items()
        }
    
    def _process_agent_response(self, response):
        """Process the streaming response from the agent"""
        try:
            event_stream = response['completion']
            agent_response = ""
            
            for event in event_stream:
                if 'chunk' in event:
                    chunk = event['chunk']
                    if 'bytes' in chunk:
                        agent_response += chunk['bytes'].decode('utf-8')
            
            return agent_response
        except Exception as e:
            return f"Error processing response: {str(e)}"
    
    def _get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()

# Usage Example
def main():
    # Initialize the agent
    telco_agent = TelcoPromptConversationAgent()
    
    # Step 1: Load your prompt data
    print("🔄 Loading prompt data...")
    if not telco_agent.load_prompt_data():
        return
    
    # Step 2: Create agent from prompt (you might need to create IAM role first)
    print("\n🔄 Creating agent from prompt...")
    if not telco_agent.create_agent_from_prompt():
        print("⚠️  Agent creation failed. You may need to create the IAM role first.")
        print("   For now, let's use direct prompt invocation...")
        
        # Alternative: Use direct prompt invocation
        return use_direct_prompt_invocation(telco_agent)
    
    # Step 3: Start conversation
    print("\n🔄 Starting conversation...")
    response, session_id = telco_agent.start_conversation_from_prompt(
        customer_id="12345",
        initial_message="I need a mobile plan with unlimited data under $60 in Australia"
    )
    
    if response:
        print(f"🤖 Agent Response: {response}")
        print(f"📝 Session ID: {session_id}")
        
        # Step 4: Continue conversation
        print("\n🔄 Continuing conversation...")
        follow_up = telco_agent.continue_prompt_conversation(
            session_id,
            "What about international roaming options?"
        )
        print(f"🤖 Follow-up Response: {follow_up}")
        
        # Step 5: Show conversation history
        print("\n📋 Conversation History:")
        history = telco_agent.get_prompt_conversation_history(session_id)
        for i, msg in enumerate(history['messages'], 1):
            print(f"{i}. {msg['role'].upper()}: {msg['content']}")
            print(f"   Time: {msg['timestamp']}")
        
        # Step 6: List all conversations
        print(f"\n📊 All Conversations: {telco_agent.list_prompt_conversations()}")

def use_direct_prompt_invocation(telco_agent):
    """Alternative method using direct prompt invocation"""
    print("\n🔄 Using direct prompt invocation as fallback...")
    
    try:
        # Use the bedrock-runtime to invoke with your prompt context
        prompt_context = telco_agent.extract_prompt_instructions()
        
        user_query = "I need a mobile plan with unlimited data under $60 in Australia"
        
        response = telco_agent.bedrock_runtime.converse(
            modelId='amazon.titan-text-express-v1',
            messages=[
                {
                    "role": "user",
                    "content": [{"text": f"Context from telco_chatbot prompt: {prompt_context}\n\nUser query: {user_query}"}]
                }
            ],
            inferenceConfig={
                "maxTokens": 1000,
                "temperature": 0.7
            }
        )
        
        assistant_response = response['output']['message']['content'][0]['text']
        print(f"🤖 Direct Prompt Response: {assistant_response}")
        
        return assistant_response
        
    except Exception as e:
        print(f"❌ Error with direct invocation: {str(e)}")
        return None

if __name__ == "__main__":
    main()
