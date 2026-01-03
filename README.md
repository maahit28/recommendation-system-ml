---

## Model Evaluation

The machine learning models used in this project are evaluated using standard
classification metrics to demonstrate understanding of the ML workflow.

### Evaluation Metrics Used
- **Accuracy**: Measures the proportion of correct predictions.
- **Confusion Matrix**: Shows the distribution of correct and incorrect
  predictions across different classes.

### Movie Genre Classification
- The movie ML model uses a small, manually created text dataset.
- A train–test split is applied before evaluation.
- Due to the limited dataset size, accuracy values may be low or unstable.
- This behavior is expected and highlights the importance of dataset size in ML.

The confusion matrix visualization helps in understanding:
- Correct predictions (diagonal values)
- Misclassifications (off-diagonal values)

### Food Taste Classification
- The food ML model predicts taste categories such as *spicy*, *sweet*, and *salty*.
- Similar evaluation methodology is followed using accuracy and confusion matrix.
- Small test sets may contain limited class diversity, affecting accuracy.

### Important Note
The objective of this project is **educational**, focusing on:
- End-to-end ML pipeline
- Proper evaluation techniques
- Honest interpretation of results

High accuracy is **not the primary goal** of this project.
