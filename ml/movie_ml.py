import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

# Dataset
texts = [
    "fight war explosion army",
    "gun chase action hero",
    "love romance relationship",
    "heartbreak emotional love",
    "funny comedy laugh jokes",
    "humor fun entertainment",
    "crime mystery suspense",
    "detective investigation thriller"
]

labels = [
    "action",
    "action",
    "romance",
    "romance",
    "comedy",
    "comedy",
    "thriller",
    "thriller"
]

# Vectorization
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)
y = labels

# Train–test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# Model training
model = MultinomialNB()
model.fit(X_train, y_train)

# Evaluation
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred, labels=model.classes_)

def predict_genre(description):
    data = vectorizer.transform([description])
    return model.predict(data)[0]

# Evaluation output (for learning / exam)
if __name__ == "__main__":
    print("Movie ML Evaluation")
    print("Accuracy:", accuracy)
    print("Confusion Matrix:")
    print(cm)

    # Plot confusion matrix
    plt.figure(figsize=(5, 4))
    plt.imshow(cm, cmap="Blues")
    plt.title("Movie Genre Confusion Matrix")
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.colorbar()

    classes = model.classes_
    plt.xticks(range(len(classes)), classes)
    plt.yticks(range(len(classes)), classes)

    for i in range(len(classes)):
        for j in range(len(classes)):
            plt.text(j, i, cm[i, j], ha="center", va="center")

    plt.tight_layout()
    plt.show()
