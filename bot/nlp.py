import openai
from config import Config

openai.api_key = Config.OPENAI_API_KEY


def process_data_with_openai(user_query, data):
    """
    Processes the user's query in conjunction with the dataset using the OpenAI API 
    to return the most relevant records, formatted directly by the API.

    This function takes a user's query and a dataset, constructs a prompt to feed 
    into the OpenAI API, and retrieves the most relevant records based on the user's request. 
    The results are returned in a specific format dictated by the prompt.

    Args:
        user_query (str): The query text provided by the user.
        data (list): The dataset fetched from the database, typically a list of tuples or dictionaries.

    Returns:
        str: The formatted response from the OpenAI API, containing the most relevant records.
    """

    # Model specification with flexibility for future changes
    model = "gpt-3.5-turbo"  # Consider using "gpt-4" depending on cost and requirements

    # Preparing messages for the model
    messages = [
        {"role": "system", "content": "You are an assistant helping to find relevant alumni information."},
        {"role": "user", "content": f"User query: '{user_query}'. Dataset: {data}. "
                                    "Provide the most relevant records, ranked from most relevant to least. "
                                    "If the user query does not specify the number of records, return 5 by default. "
                                    "Return no more than 20 records, regardless of the user query. "
                                    "Format the response as a bullet-point list with each record on a new line, like so:\n"
                                    "Here is the most relevant alumni information based on your query: \n"
                                    "- Record 1: [details]\n"
                                    "- Record 2: [details]\n"
                                    "- ...\n"}
    ]

    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
        max_tokens=1024
    )

    return response.choices[0].message.content.strip()