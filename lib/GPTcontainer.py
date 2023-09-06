import openai
#from .conversation import Conversation

openai.api_key = "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"

def get_completion(prompt, model="gpt-3.5-turbo"):
        messages = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
        )
        return response.choices[0].message["content"]


