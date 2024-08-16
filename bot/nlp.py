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
                                    
                                    "prioritize alumni with most updated information."

                                    "If the user put some questions unrelated to our data, send a reminder and tell them the data columns we have instead, and ask them to reprompt. Don't respond any alumni information in this case."
                                    "If the dataset does not explicitly contain information being asked, do not return results."
                                    "If the user question has some unknown attributes, then send a reminder that we don't have that attribute in the dataset, and ask them to reprompt. Don't respond any alumni information in this case. Examples of unknown attributes for this dataset include gender, ethnicity, age, nationality. Don't infer ethnicity/nationality from alumni's name or location."

                                    "Provide responses based on the available data and not on inferences or assumptions. For instance, don’t assume someone with a Chinese name is from China. Also, don't assume someone with a US location is from the US."

                                    "If the user query does not specify the number of alumni to return, provide 5 alumni by default, and provide a message at the end saying that 'note that we provide 5 alumni by default if a number is not specified'. However, do not include this message if you return less than 5 alumni. "
                                    "If the user specified a number, but there aren't enough alumni to return, include a sentence letting the user know that these are all the avalible alumni we can find."
                                    "If the user specify more than 8 alumni to return, do not return more than 8 alumni, and provide a message at the end saying that note that we provide 8 alumni at most per query "

                                    "Include the following details for each alumni: Name, Email, LinkedIn Profile, Company, Job Title, Location, Industry, Graduating Class, and Last Updated. "
                                    "Use 'N/A' for any information that is not available. "

                                    "If the user is asking a question that can be answered and needs specific alumni information, format the response as a structured and well-organized list, with each alumni's information formatted as follows:\n"
                                    f"Here is the alumni information based on your query: {user_query}: \n"
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
                                    "  LinkedIn: [LinkedIn URL] \n"
                                    "  Company: [Company] \n"
                                    "  Job Title: [Job Title] \n"
                                    "  Location: [Location] \n"
                                    "  Industry: [Industry] \n"
                                    "  Graduating Class: [Graduating Class] \n"
                                    "  Last Updated: [Last Updated] \n"
                                    "- ..."
                                    "However, if the user is asking a question that can be answered but does not need specific alumni information, simply provide answer to the user's question without providing alumni info in the above format. "
                                    }
    ]

    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
        max_tokens=1024
    )

    return response.choices[0].message.content.strip()