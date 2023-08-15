from config import GPT_API_TOKEN
import requests


api_key = GPT_API_TOKEN
endpoint = 'https://api.openai.com/v1/chat/completions'


def call_chatgpt(prompt):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    data = {
        'messages': [{'role': 'system', 'content': 'You are a helpful assistant.'}, {'role': 'user', 'content': "Tell me a joke that isnt about scientists"}],
        'model': 'gpt-4',  # Specify the model you want to use
        'temperature': 0
    }

    response = requests.post(endpoint, json=data, headers=headers)

    return response.json()

def main():
    prompt = "Tell me a joke."

    response_data = call_chatgpt(prompt)
    
    # Retrieve the assistant's reply from the response
    completions = response_data['choices'][0]['message']['content']

    print(completions)

if __name__ == "__main__":
    main()
