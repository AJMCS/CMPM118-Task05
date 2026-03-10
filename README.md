# CMPM118 Task 5 - Understanding Logical Reasoning

An LLM-driven Studio Ghibli knowledge base built in Prolog and queried 
via Python using pyswip. Natural language is translated into prolog and variables using an LLM, then executed against the knowledge base, and finally returned to natural laguage. This project is a reimplementatino of the Logic-LM paper (Pan et al., 2023).

## How it relates to Logic-LM Paper
- **Problem Formulator** — GPT-4o-mini translates a natural language question into a Prolog query and identifies the variables to extract.
- **Symbolic Reasoner** — SWI-Prolog runs the query against the Ghibli KB deterministically.
- **Self-Refiner** — if the query fails, the LLM receives the error and generates a corrected query up to 3 attempts.
- **Result Interpreter** — GPT-4o-mini converts the raw Prolog results into a natural language answer.

## Setup
1. Install SWI-Prolog: `brew install swi-prolog`
2. Create a virtual environment: `python3 -m venv venv`
3. Activate it: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a .env file with your OpenAI API key, titled 'OPENAI_API_KEY:your_key_here'
6. Run: `python3 ghibli.py`
