import os
import json
from openai import OpenAI
from pyswip import Prolog
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prolog = Prolog()
prolog.consult("ghibli.pl")

description = """You are a Prolog query generator for a Studio Ghibli knowledge base. 
                For every question, you are to identify and generate both the prolog and the variables for that specific query. 
                The prolog query should be as specific as possible to get the most accurate results. 
                The variables should be a list of the variables used in the prolog query that we want to extract results for.

                You will return valid json with two keys: "query" and "variables". 
                The "query" value should be a valid Prolog query string that can be run against the KB. 
                The "variables" value should be a list of the variables used in the query that we want to extract results for.

                The KB has these predicates:
                - movie(Title, Genre, Year)
                - director(Title, Director)
                - composer(Title, Composer)
                - award(Title, Award)
                - nomination(Title, Nomination)
                - top_movies(Title)  % won or nominated
                - classic(Title)    % pre-2005 + recognized
                - modern_classic(Title) % post-2015 + recognized
                - same_composer(Title1, Title2) % true if Title1 and Title2 have the same composer
                - same_director(Title1, Title2) % true if Title1 and Title2 have the same director
                - recognized(Title) % true if Title is recognized as a classic or modern classic
                
                All atoms are lowercase with underscores. For example:
                - Directors: hayao_miyazaki, isao_takahata, hiromasa_yonebayashi, yoshifumi_kondo, goro_miyazaki
                - Composers: joe_hisaishi, cecile_corbel, yuji_nomi, katsu_hoshi
                - Genres: fantasy, slice_of_life, action_adventure, drama

                Return ONLY valid json that meets the above conditions, nothing else. No explanation, no markdown, no punctuation at the end."""


def form_query(question: str) -> tuple:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": description

            },
            {
                "role":"user",
                "content": question
            }
        ]
    )

    response_text = response.choices[0].message.content.strip()
    parsed = json.loads(response_text)
    return parsed["query"], parsed["variables"]

def run_query(prolog_query: str, variables: list) -> list:
    results = list(prolog.query(prolog_query))
    if not results:
        return []
    return [tuple(r[v] for v in variables) for r in results]

def interpret_query(question: str, query: str, results: list) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role":"system",
                "content":"You are a helpful assistant that interprets Prolog query results and answer questions in plain English. Keep answers concise."
            },
            {
                "role":"user",
                "content": f"""Question: {question}
                Prolog query: {query}
                Results: {results}

                Answer the question naturally based on the results."""
            }
        ]
    )
    return response.choices[0].message.content.strip()

def refine_query(question: str, query: str, error_message: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role":"system",
                "content":description
            },
            {
                "role":"user",
                "content": f"""Question: {question}
                Prolog Query: {query}
                Error Message: {error_message}
                Refine the Prolog query to fix the error. Return ONLY the new query, no explanation, no markdown, no punctuation."""
            }
        ]
    )
    return response.choices[0].message.content.strip()

def ask(question: str, max_retries: int=3) -> str:
    query, variables = form_query(question)
    print(f"Generated query: {query}")

    for attempt in range(max_retries):
        try:
            results = run_query(query, variables)
            return interpret_query(question, query, results)
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            query = refine_query(question, query, str(e))
            print(f"Refined query: {query}")

    return "Sorry, I couldn't answer that question."

question = input("Ask a question about Ghibli films: ")
print(ask(question))