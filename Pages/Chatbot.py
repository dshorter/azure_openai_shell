# Authenticating with Entra ID - Service Principal 
# - This has two methods to get the access tokens for a given service principal
# - EDAV will setup this service principal, will provide "Role" : 
import os        
import streamlit as st    
import openai
from dotenv import load_dotenv
from azure.identity import AzureCliCredential, ChainedTokenCredential, ManagedIdentityCredential, EnvironmentCredential, get_bearer_token_provider
from openai import AzureOpenAI

load_dotenv()  

# Variables not used here do not need to be updated in your .env file
azure_openai_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
azure_openai_api_version = os.environ["AZURE_OPENAI_API_VERSION"]
azure_openai_deployment = os.environ["AZURE_OPENAI_DEPLOYMENT"]    

st.title("DRSC EDAV OpenAI Lab - Chatbot " )    
# st.header("DRSC EDAV OpenAI Lab - Chatbot " )    
# ----------------------------------------------------------
# Method-01 : access token for Service Principal 
# ----------------------------------------------------------  
credential = ChainedTokenCredential(ManagedIdentityCredential(), EnvironmentCredential(), AzureCliCredential())
access_token = credential.get_token("https://cognitiveservices.azure.com/.default")
client = AzureOpenAI(
    api_key=access_token.token,
    azure_endpoint=azure_openai_endpoint,
    api_version=azure_openai_api_version
)

#----------------------------------------------------------
# Set up UI for chat 
#---------------------------------------------------------- 
if prompt := st.text_input("Ask a question"):
    # Initialize session state messages if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
    st.write(f"**You:** {prompt}")

    # Display assistant response in chat message container
    stream = client.chat.completions.create(
        model=azure_openai_deployment,
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages  
        ],
        stream=True,
    )
    response = ""
    for chunk in stream:
        if chunk.choices:
            delta = chunk.choices[0].delta
            if delta.content:
                response += delta.content
    
    st.write(f"**Assistant:** {response}")

    st.session_state.messages.append({"role": "assistant", "content": response})


message= [
        {
            "role": "user",
            "content": "When did CDC formed ?",  
        }  
    ]
chat_completion = client.chat.completions.create(
    model=azure_openai_deployment , # model = "deployment_name" for Azure OpenAI 
    messages=message
)                                                            
print("--- using method-1 -------------")
print( chat_completion.model_dump_json())




# # ----------------------------------------------------------
# # Method #:2 :  Bearer token for Service Principal 
# # -----------------------------------------------------------
# token_provider2 = get_bearer_token_provider(
#     EnvironmentCredential(),
#     "https://cognitiveservices.azure.com/.default"
# )
# client = AzureOpenAI(
#     azure_ad_token_provider=token_provider2,
#     azure_endpoint=azure_openai_endpoint,
#     api_version=azure_openai_api_version
# )
# message= [
#         {
#             "role": "user",
#             "content": "Is cucumber a fruit",
#         }
#     ]
# chat_completion = client.chat.completions.create(
#     model=azure_openai_deployment , # model = "deployment_name" for Azure OpenAI 
#     messages=message
# )
# print("--- using method-2 -------------")
# print( chat_completion.model_dump_json())


