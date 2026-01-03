import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

food_texts = [
    "biryani chilli spicy masala",
    "pani puri chaat spicy",
    "pizza burger fries salty",
    "chips popcorn salty",
    "cake icecream chocolate sweet",
    "cookies brownie sweet"
]

food_labels = [
    "spicy",
    "spicy",
    "salty",
    "salty",
    "sweet",
    "sweet"
]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(food_texts)
y = food_labels

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=42
)

model = MultinomialNB()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)

def predict_taste(description):
    data = vectorizer.transform([description])
    return model.predict(data)[0]

if __name__ == "__main__":
    print("Food ML Evaluation")
    print("Accuracy:", accuracy)
    print("Confusion Matrix:")
    print(cm)

    # Plot confusion matrix
    plt.figure(figsize=(4, 3))
    plt.imshow(cm, cmap="Greens")
    plt.title("Food Taste Confusion Matrix")
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.colorbar()

    classes = list(set(y))
    plt.xticks(range(len(classes)), classes)
    plt.yticks(range(len(classes)), classes)

    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, cm[i, j], ha="center", va="center")

    plt.tight_layout()
    plt.show()
