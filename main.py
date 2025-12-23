from recommender import recommend_movie, recommend_food
from ml.movie_ml import predict_genre

def show_list(items):
    if not items:
        print("No recommendations found.")
    else:
        for item in items:
            print("-", item)


print("\n=== Simple Recommendation System ===")
print("1. Movie Recommendation (Rule-based)")
print("2. Food Recommendation (Rule-based)")
print("3. Movie Recommendation (ML-based)")

choice = input("Enter choice (1/2/3): ").strip()

# Rule-based movie recommendation
if choice == "1":
    print("\nAvailable genres: action, comedy, romance, thriller")
    genre = input("Enter genre: ").lower().strip()
    recommendations = recommend_movie(genre)
    show_list(recommendations)

# Rule-based food recommendation
elif choice == "2":
    print("\nAvailable tastes: spicy, sweet, salty")
    taste = input("Enter taste: ").lower().strip()
    recommendations = recommend_food(taste)
    show_list(recommendations)

# ML-based movie recommendation
elif choice == "3":
    description = input("\nDescribe the movie you want to watch: ").lower().strip()
    predicted_genre = predict_genre(description)

    print(f"\nPredicted genre: {predicted_genre}")
    recommendations = recommend_movie(predicted_genre)
    show_list(recommendations)

else:
    print("Invalid choice. Please restart the program.")
