import os
from openai import OpenAI
from pyswip import Prolog
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prolog = Prolog()
prolog.consult("ghibli.pl")



