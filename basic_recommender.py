def recommend_movie(genre):
    movies = {
        "action": ["Mad Max", "John Wick", "Avengers", "Gladiator"],
        "comedy": ["3 Idiots", "The Hangover", "PK", "Dhamaal"],
        "romance": ["Titanic", "La La Land", "Notebook", "Before Sunrise"],
        "thriller": ["Inception", "Shutter Island", "Gone Girl"]
    }
    return movies.get(genre, [])


def recommend_food(taste):
    food = {
        "spicy": ["Chilli Paneer", "Biryani", "Pav Bhaji", "Chole Bhature"],
        "sweet": ["Gulab Jamun", "Ice Cream", "Chocolate Cake", "Rasgulla"],
        "salty": ["Fries", "Popcorn", "Nachos", "Samosa"]
    }
    return food.get(taste, [])
