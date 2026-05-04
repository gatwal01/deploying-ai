from langchain.tools import tool

import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from pydantic import BaseModel, Field

#from fastmcp import FastMCP
#import sqlalchemy as sa
#import pandas as pd

#from utils.logger import get_logger
#_logs = get_logger(__name__)

from dotenv import load_dotenv
import os


load_dotenv('../../05_src/.secrets')
load_dotenv('../../05_src/.env')

vector_db_client_url="http://localhost:8000"
chroma = chromadb.HttpClient(host=vector_db_client_url)
collection = chroma.get_collection(name="pitchfork_reviews", 
                                   embedding_function=OpenAIEmbeddingFunction(
                                       api_key = os.getenv("OPENAI_API_KEY"),
                                       model_name="text-embedding-3-small")
                                   )


class MusicReviewData(BaseModel):
    """Structured music review data response."""
    title: str = Field(..., description="The title of the album.")
    artist: str = Field(..., description="The artist of the album.")
    review: str = Field(..., description="A portion of the album review that is relevant to the user query.")
    score: float = Field(None, description="The Pitchfork score of the album. The score is numeric and its scale is from 0 to 10, with 10 being the highest rating. Any album with a score greater than 8.0 is considered a must-listen; album with a score greater than 6.5 is good.")


@tool
def semantic_search(query: str, n_results: int = 1) -> list["MusicReviewData"]:
    """Fetches music review data based on the query. Returns n_results reviews."""

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
