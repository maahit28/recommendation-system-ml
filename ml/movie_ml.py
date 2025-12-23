from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Sample dataset
texts = [
    "fight war explosion",
    "love romance relationship",
    "funny comedy laugh",
    "mystery suspense crime"
]

labels = ["action", "romance", "comedy", "thriller"]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)

model = MultinomialNB()
model.fit(X, labels)

def predict_genre(description):
    data = vectorizer.transform([description])
    return model.predict(data)[0]


