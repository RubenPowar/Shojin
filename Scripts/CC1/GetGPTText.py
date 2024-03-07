from openai import OpenAI
import os
import pandas as pd
import time
from dotenv import load_dotenv

def get_completion(prompt, model="gpt-3.5-turbo"):
    # defaults to getting the key using os.environ.get("OPENAI_API_KEY")
    # if you saved the key under a different environment variable name, you can do something like:
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')

    client = OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content


def generate_location_description(location):
    prompt = f"here is an example of a description of a location in a property investment appraisal:\n\
    'North Acton is an increasingly popular area of West London, located 2.5 miles west of Notting Hill, \
     and 2.3 miles east of Ealing. \nThe area is currently seeing a high level of residential development \
     and falls within the Old Oak and Park Royal regeneration area.' please write a description in a similar \
     style for {location}. Focus on any ongoing development and be critical if necessary. Limit the response to 50 words."
    response = get_completion(prompt)
    return response

if __name__ == '__main__':
    print(generate_location_description('Mornington Crescent, Camden'))
