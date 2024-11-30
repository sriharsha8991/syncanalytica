import os
from groq import Groq

# Function to initialize the Groq client
def initialize_groq_client(api_key: str) -> Groq:
    """
    Initialize the Groq client with the provided API key.
    """
    return Groq(api_key=api_key)

# Function to generate a detailed summary and report
def generate_summary_report(client: Groq, context: str) -> str:
    """
    Generate a detailed summary and report using the Groq chat API.
    
    Args:
        client (Groq): The initialized Groq client.
        context (str): The context data to be summarized.
        model (str): The model to use for chat completions.
        
    Returns:
        str: The generated summary and report.
    """
    # Prepare the chat messages
    messages = [
        {
            "role": "user",
            "content": f"""Use the Context of the given data and produce detailed summary and report about it. 
            Comment about the columnns and their effects using, Context: {context}
            Make Sure your output is in the following format:<follow strictly everytime>
            <template>
            ### Underlying problem statement: (Possible problem statement)
            -> Analysis of the data from the given context and how it is being analysed based on the Possible problem statement 
            -> Insights in 3 major points:
            <template>
            always make sure to follow this template""",
        }
    ]
    model= "llama3-8b-8192"
    
    # Make the API call
    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model,
    )
    
    # Return the response content
    return chat_completion.choices[0].message.content