import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression

data = {
    "CGPA": [9.2, 7.5, 6.8, 8.7, 5.9, 8.0, 6.2, 7.9],
    "Projects": [3, 1, 1, 2, 0, 2, 1, 2],
    "Internship": [1, 0, 0, 1, 0, 1, 0, 1],
    "Skills": [8, 5, 4, 7, 3, 6, 4, 7],
    "Placed": [1, 0, 0, 1, 0, 1, 0, 1]
}

df = pd.DataFrame(data)
print(df)
X = df[["CGPA", "Projects", "Internship", "Skills"]]
y = df["Placed"]
model = LogisticRegression()
model.fit(X, y)
joblib.dump(model, "model.pkl")

print("Model trained and saved successfully 🚀")