from langchain.tools import tool
import json
import requests

from openai import OpenAI
client = OpenAI()

@tool
def get_jokes(n:int=1):
    """
    Returns n jokes from the Jokes API.
    https://humorapi.com/docs/
    """
    url = "https://api.humorapi.com/jokes/search"
    params = {
        "number": n,
        "max-length": 140,
        "api-key": "abcd1234"

    }
    response = requests.get(url, params=params)
    resp_dict = response.json()
    joke_list = resp_dict.get("jokes", []) 
    
    jokes = "\n".join([
        f"{i+1}. {j.get('joke', 'No joke text found')}"
        for i, j in enumerate(joke_list)
    ])

    ###
    # Uses the Moderation API to check if jokes are harmful and will append FLAGGED FOR CONTENT 
    # before the joke string
    # https://developers.openai.com/api/docs/guides/moderation
    ###

    response = client.moderations.create(
            model="omni-moderation-latest",
            input=jokes,
        )
    flagged = response.results[0].flagged

    if flagged:
        jokes = f"FLAGGED FOR CONTENT:\n{jokes}"

    return jokes

   

    

# Tried to create a separate tool, but simplified into one tool based on time
#
# @tool
# def flag_jokes(jokes: str) -> str:
#     """
#     Uses the Moderation API to check if jokes are harmful and will append FLAGGED FOR CONTENT 
#     before the joke string
#     """
#     response = client.moderations.create(
#         model="omni-moderation-latest",
#         input=jokes,
#     )
#     if (response.results[0].flagged = True)
#         {jokes = f'FLAGGED FOR CONTENT: ',{jokes}}
#     else
#         jokes 