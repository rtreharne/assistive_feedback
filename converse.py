import openai

# Set up your OpenAI API credentials
openai.api_key = 'YOUR_API_KEY'

# Define a function to have a conversation with CHAT-GPT
def chat_with_gpt(prompt):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=100,
        temperature=0.7,
        n=1,
        stop=None,
        temperature=0.7
    )
    return response.choices[0].text.strip()

# Start the conversation
print("You are now chatting with CHAT-GPT. Type 'quit' to exit.")
while True:
    user_input = input("User: ")
    if user_input.lower() == 'quit':
        break
    prompt = f"You: {user_input}\nCHAT-GPT:"
    response = chat_with_gpt(prompt)
    print(response)
