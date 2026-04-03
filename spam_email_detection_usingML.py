# ================================
# Spam Classification Project
# ================================

# 1. Import Libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, f1_score

# ================================
# 2. Load Dataset
# ================================
df = pd.read_csv("spam.csv", encoding='latin-1')

# Your dataset columns: label, text
df = df[['label', 'text']]

# Rename for consistency
df.rename(columns={'text': 'message'}, inplace=True)

# ================================
# 3. Data Preprocessing
# ================================

# Encode labels (ham=0, spam=1)
le = LabelEncoder()
df['label'] = le.fit_transform(df['label'])

# Convert text → numerical using TF-IDF
vectorizer = TfidfVectorizer(max_features=3000)
X = vectorizer.fit_transform(df['message'])
y = df['label']

# ================================
# 4. Train-Test Split
# ================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ================================
# 5. Naive Bayes Model
# ================================
nb_model = MultinomialNB()
nb_model.fit(X_train, y_train)

y_pred_nb = nb_model.predict(X_test)

print("===== Naive Bayes =====")
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred_nb))
print("F1 Score:", f1_score(y_test, y_pred_nb))

# ================================
# 6. SVM Model
# ================================
svm_model = SVC(kernel='linear')
svm_model.fit(X_train, y_train)

y_pred_svm = svm_model.predict(X_test)

print("\n===== SVM =====")
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred_svm))
print("F1 Score:", f1_score(y_test, y_pred_svm))

# ================================
# 7. Test with Custom Input
# ================================
sample = ["Congratulations! You won a free iPhone"]
sample_vec = vectorizer.transform(sample)

nb_pred = nb_model.predict(sample_vec)
svm_pred = svm_model.predict(sample_vec)

# Convert numeric → label
label_map = {0: "Ham (Not Spam)", 1: "Spam"}

print("\n===== Sample Test =====")
print("Message:", sample[0])

print("\nNaive Bayes Prediction:")
print("Raw Output:", nb_pred)
print("Label:", label_map[nb_pred[0]])

print("\nSVM Prediction:")
print("Raw Output:", svm_pred)
print("Label:", label_map[svm_pred[0]])

if f1_score(y_test, y_pred_svm) > f1_score(y_test, y_pred_nb):
    print("\nSVM performs better based on F1 Score")
else:
    print("\nNaive Bayes performs better based on F1 Score")
