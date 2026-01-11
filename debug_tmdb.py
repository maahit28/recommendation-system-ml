from tmdb_client import fetch_movies

df = fetch_movies("movie", "action", "hollywood")

print(df.head())
print("Total results:", len(df))
