# from langchain.chat_models import AzureChatOpenAI
# from langchain.schema import HumanMessage

# BASE_URL = "https://chaud-m4bwiifx-eastus2.openai.azure.com/"
# API_KEY = "46z847AGFiOqdlWxzaYuQ0Ad9XbCwm9o6qqKXPZPvpAdoIa9tlaKJQQJ99ALACHYHv6XJ3w3AAAAACOGjxTF"
# DEPLOYMENT_NAME = "gpt-4"

# model = AzureChatOpenAI(
#     openai_api_base=BASE_URL,
#     openai_api_version="2024-08-01-preview",
#     deployment_name=DEPLOYMENT_NAME,
#     openai_api_key=API_KEY,
#     openai_api_type="azure",
# )

# print(model(
#     [
#         HumanMessage(
#             content="Translate this sentence from English to French. I love programming."
#         )
#     ]
# ))

import os
from openai import AzureOpenAI

client = AzureOpenAI(
  azure_endpoint = "https://chaud-m4bwiifx-eastus2.openai.azure.com/", 
  api_key="46z847AGFiOqdlWxzaYuQ0Ad9XbCwm9o6qqKXPZPvpAdoIa9tlaKJQQJ99ALACHYHv6XJ3w3AAAAACOGjxTF",  
  api_version="2024-08-01-preview"
)

response = client.chat.completions.create(
    model="gpt-4", # model = "deployment_name".
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Does Azure OpenAI support customer managed keys?"},
        {"role": "assistant", "content": "Yes, customer managed keys are supported by Azure OpenAI."},
        {"role": "user", "content": "Do other Azure AI services support this too?"}
    ]
)

print(response.choices[0].message.content)