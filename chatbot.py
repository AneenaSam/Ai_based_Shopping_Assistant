import os
from groq import Groq


SYSTEM_PROMPT = """
You are a helpful AI supermarket shopping assistant.
Suggest products based on budget, category, and user needs.
Keep answers short and practical.
Mention approximate prices in INR.
"""

def shopping_bot(user_input, context):

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "system", "content": context},
        {"role": "user", "content": user_input},
    ]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.7,
        max_tokens=300,
    )

    return response.choices[0].message.content