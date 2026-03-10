from pyswip import Prolog

prolog = Prolog()
prolog.consult("ghibli.pl")

def query(description: str, query: str, var: str = None):
    """Run prolog queries ad print results."""

    print(f"\n{'='*55}")
    print(f"Query: {description}")
    print(f"Query Function: {query}")
    print("-" * 55)
    results = list(prolog.query(query))
    if not results:
        print("  (no results)")
    elif var is None:
        # Boolean / ground query
        print(f"  true  ({len(results)} solution(s))")
    else:
        for r in results:
            if isinstance(var, list):
                row = ", ".join(f"{v}={r[v]}" for v in var)
                print(f"  {row}")
            else:
                print(f"  {r[var]}")
    return results


# Query all movies and their genres
query("All movies and their genres", "movie(X, Genre, _)", var=["X", "Genre"])

# Query all award winning movies
query("Award winning movies", "distinct(X, award(X, _))", var="X")

# Query all nominated movies
query("Nominated movies", "distinct(X, nomination(X, _))", var="X")

# Query the top movies (won OR nominated)
query("Top movies", "distinct(X, top_movies(X))", var="X")

# Query classic movies (pre-2005 + recognized)
query("Classic movies", "distinct(X, classic(X))", var="X")

# Query modern classics (post-2015 + recognized)
query("Modern classics", "distinct(X, modern_classic(X))", var="X")

# Query all Hayao Miyazaki movies
query("Hayao Miyazaki films", "director(X, hayao_miyazaki)", var="X")

# Query movies with same composer as spirited_away
query("Same composer as Spirited Away", "same_composer(spirited_away, Y)", var="Y")

# Query movies in the fantasy genre
query("Fantasy movies", "movie(X, fantasy, _)", var="X")

# Query all movies with their director and composer
query("Movies with director and composer", "movie(X,_,_), director(X,D), composer(X,C)", var=["X","D","C"])


print("\n" + "=" * 55)
print("All queries completed successfully.")