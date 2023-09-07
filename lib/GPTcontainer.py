import openai
from lib.apiKey import key

openai.api_key = key

def get_completion(prompt, model="gpt-3.5-turbo"):
        print(prompt)
        messages = [{"role": "system", "content": prompt}]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
        )
        return response.choices[0].message["content"]


