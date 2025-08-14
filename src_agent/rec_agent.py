import boto3
import json
import os
from datetime import datetime, timedelta
from botocore.config import Config

# Set your API key
os.environ['AWS_BEARER_TOKEN_BEDROCK'] = "bedrock-api-key-YmVkcm9jay5hbWF6b25hd3MuY29tLz9BY3Rpb249Q2FsbFdpdGhCZWFyZXJUb2tlbiZYLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFTSUE2RlJYWEdMS09FRzVZRkkyJTJGMjAyNTA4MTQlMkZ1cy13ZXN0LTIlMkZiZWRyb2NrJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNTA4MTRUMDExMzIzWiZYLUFtei1FeHBpcmVzPTQzMjAwJlgtQW16LVNlY3VyaXR5LVRva2VuPUlRb0piM0pwWjJsdVgyVmpFUEglMkYlMkYlMkYlMkYlMkYlMkYlMkYlMkYlMkYlMkZ3RWFDWFZ6TFhkbGMzUXRNaUpHTUVRQ0lGWCUyQmtXOVRMbEVjbFkyZiUyQmd3dG91bHNnbGFFYlFDZTBIbVR6UU92d2RJaEFpQU9DRWZ3WnBQYjI4WmJCNmQ5Y0VaWnpjVUlURnAzaFEyQlVZJTJCVHhPeW5yeXEwQXdnNkVBSWFERGszTkRBd01EWTVPREEyT0NJTXE3cDZFaDlUQ3hidTRrWkdLcEVER000UGxpVmJiWHFzNmpSNndza0RjZ1FyWWd1UGdxY0hRelFMQ1Exdk5RZWhRTThNY3hJMFl3bTBFVmh0UEJMVG9tWmNZaEs5UVBiamtJJTJGUWRIQ3lZTVZDSW9XMUpjJTJGV2NMUHclMkJIYUUlMkIyJTJCTjl6MiUyRjJnSHV4dGglMkZXNk9mZ1FsS0h3dzA0c2VqRUNlYnBRWTU2d2x5eHc0RGp5THdnRzFOTFlHR3c5b0wlMkY5VU9VaEZZbmplbFIxSTZXNU02RlM0eG8yN1daYjF1eUtLTkZJS0VrNnR0cUdsakhHeFRIcWhBT1FRenY4ZWpBaEtKUkdldzZvWXczTSUyQnlKNlNLdEFuNlVicFR4TVFraG1MdThmJTJGeG42SVZqQUdxViUyQmlLUkF0ZSUyRnNldHVYbVBzU1hJZnNKMG5hcGZKa3pvaVJJSFg3bTFDeUlBMk02Y2IlMkZUR2VHWFUlMkZnNWJPNFNZaUNjc21wNkZUJTJGcUE1bk40UTRYM0NWMXIzTTdoZDR5VGF3JTJCTjUlMkZkNlQzd2gwcmp4TXMlMkJuMlJvcDkyQ1Q1R0pGUFRsbEJ2WndETG4xc1RqZXVsdTBndU50QXV1QjRUTjZOM0l0Tm1GcVd2cmlWNWRuSGNaUnNhQTkxU3BmZFZWNFJsRnE4JTJGeXZRWjU5VzRkMSUyRm5hJTJGdE1QSWhPZCUyQkJicWQ5eWNkZ05RaldKdXFXMVZlNE1vZkF1JTJCZzJ4RlFTM2N3NGNuMHhBWTZ1QUxqZW5EamJ6Q2RqZkRaaGF0U0hsRXZkbnZsYmpQSE5mZ3QlMkZ0TjBFJTJCZ0pjc0R6U3VHVU1IaXpzQVNlYVFkd3RQQUh4Y1lQS3VEUGZuWFlpNjhMRzhuSWJjSDdzUlFPaFlFQmdwWGJkRVVyWTlidkhGTGF1TE1xdWkzclN2Y1BCVWlrJTJCYTBqY2FTUnVscUJzJTJCZTB6UGtSazU0N3ZPMHo1NHdGdXFVTG5FZjdla3hObE5pZTRkaE5iNzJ1SSUyRlNPWUtvMTN4TVp0SXYzZnZXYU5FV002Sk0lMkI2cElWYiUyRjBtTG1ERDFMYm9LcUxVc2tIRDRPZEF6M1g0VnRKUXBxbDBKQkFGcGg0azRaMHpKa3YwaEZRNXJJWnFWeDRiNTRKdm8xVmhGeTZvbm13MHNuanNSRjJEdVA4QW9BYyUyRmdMSWhQZzFpYnJrYnV2RHhmY1Z1ZzVhNDNpTE5XOGIxSTJpSFNwT3FQQ1lYVmYlMkJVOUNQVXRqTkVseHVtQ1hUVUZTbDdQYWFHWXZKc3MxaiUyRmxaM0poTWFveDJNS2owOXFuM1NpTFlzJTNEJlgtQW16LVNpZ25hdHVyZT1hZDA1Y2QxYzAzNDNkN2QxMjFiNzhlZjg2MjEwMGI1YTIxOTVjMTBjZGY2ZDBiY2Y4NmU2NWI4YjgwODNhYjJkJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZWZXJzaW9uPTE="

# Mock conversation data
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

class ExistingTelcoAgent:
    def __init__(self):
        self.prompt_arn = "arn:aws:bedrock:us-west-2:974000698068:prompt/S8TPWVPSX3"
        self.agent_arn = "arn:aws:bedrock:us-west-2:974000698068:agent/0IHZAOOCNZ"
        self.agent_id = "0IHZAOOCNZ"  # Extracted from ARN
        
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
        
        self.conversations = {}
        self.mock_context = MOCK_CONVERSATION_1
    
    def get_existing_agent_info(self):
        """Get information about the existing agent"""
        try:
            response = self.bedrock_agent.get_agent(
                agentId=self.agent_id
            )
            
            agent_info = response['agent']
            print(f"✅ Found existing agent:")
            print(f"   Name: {agent_info['agentName']}")
            print(f"   ARN: {agent_info['agentArn']}")
            print(f"   Status: {agent_info['agentStatus']}")
            print(f"   Model: {agent_info.get('foundationModel', 'N/A')}")
            print(f"   Created: {agent_info.get('createdAt', 'N/A')}")
            
            return agent_info
            
        except Exception as e:
            print(f"❌ Error getting agent info: {str(e)}")
            return None
    
    def list_agent_aliases(self):
        """List available aliases for the agent"""
        try:
            response = self.bedrock_agent.list_agent_aliases(
                agentId=self.agent_id
            )
            
            aliases = response.get('agentAliasSummaries', [])
            print(f"\n📋 Available Agent Aliases:")
            for alias in aliases:
                print(f"   - {alias['agentAliasName']} (ID: {alias['agentAliasId']})")
                print(f"     Status: {alias['agentAliasStatus']}")
            
            return aliases
            
        except Exception as e:
            print(f"❌ Error listing aliases: {str(e)}")
            return []
    
    def start_conversation_with_existing_agent(self, customer_id, user_message, agent_alias_id='TSTALIASID'):
        """Start conversation with existing agent using mock context"""
        session_id = f"existing-agent-session-{customer_id}"
        
        try:
            # Prepare message with context
            contextual_message = f"""CONTEXT FROM PREVIOUS SUCCESSFUL CONVERSATION:
{self.mock_context}

---

NEW CUSTOMER INQUIRY: {user_message}

Please use the context above to provide similar quality recommendations and detailed information."""
            
            print(f"🔄 Starting conversation with agent {self.agent_id}...")
            
            response = self.bedrock_agent_runtime.invoke_agent(
                agentId=self.agent_id,
                agentAliasId=agent_alias_id,
                sessionId=session_id,
                inputText=contextual_message
            )
            
            agent_response = self._process_agent_response(response)
            
            # Store conversation
            self.conversations[session_id] = {
                'customer_id': customer_id,
                'agent_id': self.agent_id,
                'agent_arn': self.agent_arn,
                'alias_id': agent_alias_id,
                'messages': [
                    {'role': 'user', 'content': user_message, 'timestamp': self._get_timestamp()},
                    {'role': 'agent', 'content': agent_response, 'timestamp': self._get_timestamp()}
                ],
                'context_provided': True,
                'mock_context_used': 'MOCK_CONVERSATION_1'
            }
            
            return agent_response, session_id
            
        except Exception as e:
            print(f"❌ Error starting conversation: {str(e)}")
            return None, None
    
    def continue_conversation_with_context(self, session_id, user_message, agent_alias_id='TSTALIASID'):
        """Continue conversation with the existing agent"""
        if session_id not in self.conversations:
            return "❌ Session not found. Please start a new conversation."
        
        try:
            response = self.bedrock_agent_runtime.invoke_agent(
                agentId=self.agent_id,
                agentAliasId=agent_alias_id,
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
    
    def provide_context_only(self, agent_alias_id='TSTALIASID'):
        """Send only the mock context to the agent for learning"""
        context_session_id = f"context-training-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            context_message = f"""TRAINING CONTEXT - Please learn from this successful telco conversation:

{self.mock_context}

This conversation shows the ideal way to:
1. Understand customer budget and needs
2. Recommend 2-3 suitable options with specific details
3. Explain unique benefits (like grocery discounts)
4. Provide clear sign-up instructions
5. Offer ongoing assistance

Please use this as a reference for future customer interactions."""
            
            response = self.bedrock_agent_runtime.invoke_agent(
                agentId=self.agent_id,
                agentAliasId=agent_alias_id,
                sessionId=context_session_id,
                inputText=context_message
            )
            
            agent_response = self._process_agent_response(response)
            print(f"✅ Context provided to agent. Response: {agent_response}")
            
            return agent_response
            
        except Exception as e:
            print(f"❌ Error providing context: {str(e)}")
            return None
    
    def get_conversation_history(self, session_id):
        """Get conversation history for a session"""
        return self.conversations.get(session_id, None)
    
    def list_all_conversations(self):
        """List all conversations with the existing agent"""
        return {
            session_id: {
                'customer_id': conv['customer_id'],
                'message_count': len(conv['messages']),
                'context_used': conv.get('context_provided', False),
                'last_message_time': conv['messages'][-1]['timestamp'] if conv['messages'] else None
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
        return datetime.now().isoformat()
    
    def display_mock_context(self):
        """Display the mock context being used"""
        print("📋 MOCK CONTEXT TO BE PROVIDED:")
        print("=" * 60)
        print(self.mock_context)
        print("=" * 60)

# Usage Example
def main():
    # Initialize with existing agent
    telco_agent = ExistingTelcoAgent()
    
    # Display the context
    telco_agent.display_mock_context()
    
    # Step 1: Get existing agent information
    print("\n🔄 Getting existing agent information...")
    agent_info = telco_agent.get_existing_agent_info()
    
    if not agent_info:
        print("❌ Could not retrieve agent information. Check the agent ARN.")
        return
    
    # Step 2: List available aliases
    print("\n🔄 Listing agent aliases...")
    aliases = telco_agent.list_agent_aliases()
    
    # Step 3: Provide context to the agent (optional training step)
    print("\n🔄 Providing mock context to agent...")
    context_response = telco_agent.provide_context_only()
    
    # Step 4: Start a new conversation with context
    print("\n🔄 Starting conversation with existing agent...")
    response, session_id = telco_agent.start_conversation_with_existing_agent(
        customer_id="new_customer_002",
        user_message="I'm a student looking for a cheap plan with good data for streaming and social media"
    )
    
    if response:
        print(f"\n🤖 Agent Response:\n{response}")
        
        # Step 5: Continue the conversation
        print("\n🔄 Continuing conversation...")
        follow_up = telco_agent.continue_conversation_with_context(
            session_id,
            "Which network has the best coverage for university campuses?"
        )
        print(f"\n🤖 Follow-up Response:\n{follow_up}")
        
        # Step 6: Show conversation summary
        print(f"\n📊 Conversation Summary:")
        history = telco_agent.get_conversation_history(session_id)
        if history:
            print(f"   Customer: {history['customer_id']}")
            print(f"   Messages: {len(history['messages'])}")
            print(f"   Context Used: {history['context_provided']}")
            print(f"   Agent ARN: {history['agent_arn']}")
    
    # Step 7: List all conversations
    print(f"\n📋 All Conversations: {telco_agent.list_all_conversations()}")

# Alternative: Direct context injection method
def inject_context_directly():
    """Alternative method to inject context more directly"""
    telco_agent = ExistingTelcoAgent()
    
    # Test with direct context in user message
    user_message_with_context = f"""Based on this previous successful conversation:

{MOCK_CONVERSATION_1}

I need help with a similar request: I'm looking for a mobile plan around $40 with good data and some extra benefits like the Woolworths plan mentioned above. Can you recommend something similar?"""
    
    response, session_id = telco_agent.start_conversation_with_existing_agent(
        customer_id="context_test_001",
        user_message=user_message_with_context
    )
    
    if response:
        print(f"🤖 Direct Context Response:\n{response}")

if __name__ == "__main__":
    main()
    
    # Uncomment to test direct context injection
    # print("\n" + "="*60)
    # print("TESTING DIRECT CONTEXT INJECTION:")
    # inject_context_directly()
