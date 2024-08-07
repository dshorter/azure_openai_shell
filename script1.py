import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from openai import AzureOpenAI

# Load environment variables from .env file
load_dotenv()

# Debug: Print loaded environment variables
print("Loaded environment variables:")
print("AZURE_OPENAI_ENDPOINT:", os.getenv("AZURE_OPENAI_ENDPOINT"))    
print("AZURE_OPENAI_API_KEY:", os.getenv("AZURE_OPENAI_API_KEY"))    
print("AZURE_OPENAI_API_VERSION:", os.getenv("AZURE_OPENAI_API_VERSION"))
print("AZURE_OPENAI_DEPLOYMENT_NAME:", os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"))
  
azure_openai_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
# azure_openai_key = os.environ["AZURE_OPENAI_API_KEY"] 
azure_openai_api_version = os.environ["AZURE_OPENAI_API_VERSION"]
azure_openai_deployment_name  = os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]


# Set up the credentials
credential = DefaultAzureCredential()

# Initialize the Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION") #,
    # azure_ad_token_provider=credential
)

def generate_text(prompt):
    """
    Generate text using the Azure OpenAI API.
    """
    try:
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def main():
    print("Azure OpenAI API Test")
    print("---------------------")

    while True:
        user_input = input("\nEnter your prompt (or 'quit' to exit): ")
        if user_input.lower() == 'quit':
            break

        response = generate_text(user_input)
        if response:
            print("\nAI Response:")
            print(response)

if __name__ == "__main__":
    main()
