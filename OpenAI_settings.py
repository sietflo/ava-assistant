from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI()

conversation = []

def char_model(user_prompt):
    global conversation
    conversation.append({"role": "user", "content": user_prompt})
    
    completion = client.chat.completions.create(  
        model="gpt-3.5-turbo",
        messages=conversation,
        temperature=0.7,
        max_tokens=100,
        top_p=1,
        n=1
    )

    response = completion.choices[0].message.content
    
    conversation.append({"role": "system", "content": response})
    print(response)
    return response
