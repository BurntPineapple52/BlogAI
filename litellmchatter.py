from litellm import completion
import os
import json

from dotenv import load_dotenv

load_dotenv()

os.environ['GEMINI_API_KEY'] = os.getenv("GEMINI_API_KEY")

messages = []  # Initialize an empty list to store messages

try:
    while True:
        user_input = input("You: ")
        if user_input.strip() == "/quit":
            break  # Exit the loop if the user types '/quit'

        messages.append({"role": "user", "content": user_input})  # Append user message

        response = completion(
            model="gemini/gemini-2.0-flash",
            messages=messages  # Pass the entire message history
        )

        generated_text = response.choices[0].message.content
        print("Assistant:", generated_text)

        messages.append({"role": "assistant", "content": generated_text})  # Append assistant message

except Exception as e:
    print(f"An error occurred: {e}")
