import os
from openai import OpenAI
from pyswip import Prolog
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prolog = Prolog()
prolog.consult("ghibli.pl")


def form_query(question: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """You are a Prolog query generator for a Studio Ghibli knowledge base.
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
                
                Return ONLY a valid Prolog query string, nothing else. No explanation, no markdown, no punctuation at the end."""

            },
            {
                "role":"user",
                "content": question
            }
        ]
    )

    return response.choices[0].message.content.strip()

question = "Which movies were directed by Hayao Miyazaki?"
query = form_query(question)
print(query)