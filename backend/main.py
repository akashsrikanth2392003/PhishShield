import pandas as pd
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

# Initialize tqdm for pandas operations
tqdm.pandas()

# Load multiple datasets with progress bar
file_paths = [
    r'C:\Users\akash\Downloads\MakeUC2024-NewMain\data\emails.csv',  # original dataset
    r'C:\Users\akash\Downloads\MakeUC2024-NewMain\data\Phishing_Email.csv',
    r'C:\Users\akash\Downloads\MakeUC2024-NewMain\data\CEAS_08.csv',
    r'C:\Users\akash\Downloads\MakeUC2024-NewMain\data\phishing_data_by_type.csv'
    ]

print("Loading datasets...")
data_frames = [pd.read_csv(file_path) for file_path in tqdm(file_paths, desc="Reading files")]
data = pd.concat(data_frames, ignore_index=True)

# Check for NaN values in the 'Email Text' column and drop rows with missing values
print("Checking for NaN values in 'Email Text' column before dropping:", data['Email Text'].isna().sum())
data = data.dropna(subset=['Email Text'])

# Preprocess the email text
print("Preprocessing email texts...")
data['Email Text'] = data['Email Text'].progress_apply(lambda x: x.lower())

# Ensure consistent labeling across datasets
data['Email Type'] = data['Email Type'].map({'Safe Email': 0, 'Phishing Email': 1})

# Split data into training and testing sets
X = data['Email Text']
y = data['Email Type']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Vectorize the email text using TF-IDF with a progress bar
print("Vectorizing email text...")
vectorizer = TfidfVectorizer(stop_words='english', max_features=3000)  # Increased max_features for better performance
X_train_tfidf = vectorizer.fit_transform(tqdm(X_train, desc="Fitting vectorizer on training data"))
X_test_tfidf = vectorizer.transform(tqdm(X_test, desc="Transforming test data"))

# Train a Logistic Regression model
print("Training the Logistic Regression model...")
model = LogisticRegression(max_iter=1000)  # Increased max_iter for convergence
model.fit(X_train_tfidf, y_train)

# Make predictions on the test set
print("Making predictions on the test set...")
y_pred = model.predict(X_test_tfidf)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# Save the trained model and vectorizer
print("Saving model and vectorizer...")
joblib.dump(model, r'C:\Users\akash\Downloads\MakeUC2024-NewMain\logistic_regression_model.joblib')
joblib.dump(vectorizer, r'C:\Users\akash\Downloads\MakeUC2024-NewMain\vectorizer.joblib')