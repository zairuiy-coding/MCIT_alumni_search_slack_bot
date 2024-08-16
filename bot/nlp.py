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
        {"role": "user", "content": f"User query: '{user_query}'. Dataset: {data}.\n"
                                    
                                    "Prioritize alumni with the most updated information.\n"

                                    "If the user's query is unrelated to our data, send a reminder with the available data columns and ask them to reprompt. Do not provide any alumni information in this case.\n"
                                    "If the dataset does not explicitly contain the requested information, notify the user that the information is not available and do not return any results.\n"
                                    "If the user query includes unknown attributes (e.g., gender, ethnicity, age, nationality), inform them that these attributes are not in the dataset and ask them to reprompt. Do not infer attributes from existing data, and do not return alumni information in this case.\n"
                                
                                    "Provide responses based on the available data and not on inferences or assumptions. For instance, don’t assume someone with a Chinese name is from China, or someone with a US location is from the US.\n"

                                    "If the user query does not specify the number of alumni to return and at least 5 alumni are found, provide 5 alumni by default and include a note: 'Note that we provide 5 alumni by default if a number is not specified.' If fewer than 5 alumni are found, return those with the message, 'These are all the alumni we can find based on your query.'\n"
                                    "If the user specifies a number of alumni but fewer are available, include a message saying, 'These are all the alumni we can find based on your query.'\n"
                                    "If the user specifies more than 8 alumni, and 8 or more are found, return 8 alumni and include a note stating, 'Note that we provide 8 alumni at most per query.' However, if fewer than 8 alumni are found, return those with the message, 'These are all the alumni we can find based on your query.'\n"

                                    "Include the following details for each alumni: Name, Email, LinkedIn Profile, Company, Job Title, Location, Industry, Graduating Class, and Last Updated.\n"
                                    "Use 'N/A' for any information that is not available.\n"

                                    "If the user is asking a question that requires specific alumni information, format the response as a structured and well-organized list, with each alumni's information formatted as follows:\n"
                                    "Pay special attention to displaying the LinkedIn URL as plain text, not as a clickable link, and avoid displaying the URL twice.\n"
                                    f"Here is the alumni information based on your query '{user_query}':\n"
                                    "- Alumni 1: [Name]\n"
                                    "  Email: [Email]\n"
                                    "  LinkedIn: [LinkedIn URL]\n"
                                    "  Company: [Company]\n"
                                    "  Job Title: [Job Title]\n"
                                    "  Location: [Location]\n"
                                    "  Industry: [Industry]\n"
                                    "  Graduating Class: [Graduating Class]\n"
                                    "  Last Updated: [Last Updated]\n"
                                    "- Alumni 2: [Name]\n"
                                    "  Email: [Email]\n"
                                    "  LinkedIn: [LinkedIn URL]\n"
                                    "  Company: [Company]\n"
                                    "  Job Title: [Job Title]\n"
                                    "  Location: [Location]\n"
                                    "  Industry: [Industry]\n"
                                    "  Graduating Class: [Graduating Class]\n"
                                    "  Last Updated: [Last Updated]\n"
                                    "- ..."
                                    "If the user's question can be answered without providing specific alumni information, simply answer the user's question without including alumni details in the above format."
                                    }
    ]

    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
        max_tokens=1024
    )

    return response.choices[0].message.content.strip()