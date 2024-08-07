# import the OpenAI Python library for calling the OpenAI API
from openai import OpenAI
import os
import json

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

MODEL = "gpt-4o-mini"

search_query = "I want sushi somewhere that I can sit outside and has free wifi. Also I want to be able to bring my dog. Also I want a nice view!"


response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "user", "content": f"Extract keywords from this text to be used to search the Google Places API: '{search_query}'. Respond *only* with a JSON object containing the keywords, nothing else, no annotations."},
    ],
    temperature=0,
)

prompt_response = response.choices[0].message.content

if prompt_response.startswith('```json'):
    prompt_response = prompt_response[7:].strip()
if prompt_response.endswith('```'):
    prompt_response = prompt_response[:-3].strip()

response_dict = json.loads(prompt_response)
keywords = response_dict.get('keywords')

if __name__ == '__main__':
    print(keywords)