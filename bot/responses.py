import openai
from config import Config

openai.api_key = Config.OPENAI_API_KEY

def generate_response(results):
    """
    Generates a human-readable response using OpenAI based on the results.

    Args:
        results (list): A list of tuples containing alumni information.

    Returns:
        str: A generated response string.
    """
    names = ", ".join([f"{r[0]} from {r[1]}" for r in results])
    prompt = f"Generate a human-readable response listing the following people and their companies: {names}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text.strip()
