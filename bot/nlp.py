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
    model = "gpt-4o"  # Consider using "gpt-4" depending on cost and requirements

    # Preparing messages for the model
    messages = [
        {"role": "system", "content": "You are an assistant that helps users find the most relevant alumni information from the provided dataset."},
        {"role": "user", "content": f"User query: '{user_query}'. Dataset: {data}. "

                                    "prioritize most updated alumni"

                                    "Prioritize alumni who are currently working at or have previously worked at the company mentioned in the query. "
                                    "If the user specifies other priorities (such as location, job title, etc.), consider those priorities in the ranking. "

                                    "If the user query does not specify the number of alumni to return, provide 5 alumni by default. "
                                    "Do not return more than 20 alumni, regardless of the query. "

                                    "Include the following details for each alumni: Name, Email, LinkedIn Profile, Company, Job Title, Location, Industry, Graduating Class, and Last Updated. "
                                    "Use 'N/A' for any information that is not available. "

                                    "Format the response as a structured and well-organized list, with each alumni's information formatted as follows:\n"
                                    "Here is the alumni information based on your query, ranked from most relevant to least:\n"
                                    "- Alumni 1: [Name] \n"
                                    "  Email: [Email] \n"
                                    "  LinkedIn: [LinkedIn Profile URL] \n"
                                    "  Company: [Company] \n"
                                    "  Job Title: [Job Title] \n"
                                    "  Location: [Location] \n"
                                    "  Industry: [Industry] \n"
                                    "  Graduating Class: [Graduating Class] \n"
                                    "  Last Updated: [Last Updated] \n"
                                    "- Alumni 2: [Name] \n"
                                    "  Email: [Email] \n"
                                    "  LinkedIn: [LinkedIn Profile URL] \n"
                                    "  Company: [Company] \n"
                                    "  Job Title: [Job Title] \n"
                                    "  Location: [Location] \n"
                                    "  Industry: [Industry] \n"
                                    "  Graduating Class: [Graduating Class] \n"
                                    "  Last Updated: [Last Updated] \n"
                                    "- ..."}
    ]

    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
        max_tokens=1024
    )

    return response.choices[0].message.content.strip()