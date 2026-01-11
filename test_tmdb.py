from tmdb_client import fetch_movies

df = fetch_movies(
    content_type="movie",
    genre="romance",
    region="korean",
    pages=2
)

print(df.head())
print(len(df))
