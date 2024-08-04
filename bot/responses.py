from openai import OpenAI
import os
from config import Config

def generate_response(results):
    """
    Generates a human-readable response using OpenAI based on the results.

    Args:
        results (list): A list of tuples containing alumni information.

    Returns:
        str: A generated response string.
    """
    # Initialize the OpenAI client
    client = OpenAI(api_key=Config.OPENAI_API_KEY)

    # Specify the model
    model = "gpt-3.5-turbo"  # You can change this to "gpt-4", but keep the cost in mind since it can get at least 20 times more expensive compared to gpt-3.5

    # The results for analysis
    # Joins results (which is an array of tuples) into a comma separated string
    # e.g. [("Allen", "Amazon"), ("Bob", "Facebook"), ("Carol, "Google")]
    # to
    # "Allen from Amazon, Bob from Facebook, Carol from Google"
    names = ", ".join([f"{r[0]} from {r[1]}" for r in results])

    # Preparing messages for the model
    messages = [
        {"role": "system", "content": "You are an search engine"},
        {"role": "user", "content": f"Generate a human-readable response listing the following people and their companies: {names}"}
    ]

    # Sending the request to the model
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    )

    # Extracting and printing the response
    return response.choices[0].message.content.strip()