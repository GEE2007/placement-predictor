import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

df = pd.read_csv("data/student_placement.csv")

X = df[['cgpa', 'internships', 'projects_count', 'coding_skills', 'certifications', 'aptitude_score']]
y = df['placement_status']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

model = Pipeline([
    ("scaler", StandardScaler()),
    ("model", RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        random_state=42
    ))
])

model.fit(X_train, y_train)


pred = model.predict(X_test)
accuracy = accuracy_score(y_test, pred)
print(f"Model Accuracy: {accuracy:.2%}")

from sklearn.metrics import classification_report
print("\nClassification Report:")
print(classification_report(y_test, pred, target_names=["Not Placed", "Placed"]))

joblib.dump(model, "model.pkl")

print("Model trained and saved 🚀")