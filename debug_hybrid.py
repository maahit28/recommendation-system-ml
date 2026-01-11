from hybrid import HybridMovieRecommender

model = HybridMovieRecommender()
df = model.recommend("action hollywood movie")

print(df.head())
print("Total results:", len(df))
