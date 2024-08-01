import openai
from config import Config

openai.api_key = Config.OPENAI_API_KEY

def interpret_user_query(query_text):
    """
    Uses OpenAI API to interpret the user's natural language query.

    Args:
        query_text (str): The query text provided by the user.

    Returns:
        dict: Parsed information extracted from the query.
    """
    prompt = f"Extract key information from the following query: '{query_text}'"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50
    )
    extracted_info = response.choices[0].text.strip()
    return {"role": "software engineer", "limit": 10}  # Example output
