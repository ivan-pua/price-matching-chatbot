import streamlit as st
import boto3
import json

st.title('Find your Preferred Mobile Plan 📲')
st.caption('This is a simple app to find the best mobile plan for you.')

# Set AWS Bedrock client
client = boto3.client('bedrock-runtime', region_name='us-east-1')

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = client.invoke_model(
            modelId="us.anthropic.claude-sonnet-4-20250514-v1:0",
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4096,
                "messages": [{"role": "user", "content": prompt}]
            })
        )
        result = json.loads(response['body'].read())
        content = result['content'][0]['text']
        st.markdown(content)
        st.session_state.messages.append({"role": "assistant", "content": content})