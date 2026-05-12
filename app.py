import streamlit as st
import joblib
import numpy as np

# load trained model
model = joblib.load("model.pkl")

# UI title
st.title("🎯 Placement Predictor")

st.write("Enter student details below to predict placement chances")

# inputs
cgpa = st.number_input("CGPA", min_value=0.0, max_value=10.0, step=0.1)
projects = st.number_input("Number of Projects", min_value=0, step=1)
internship = st.number_input("Internship (1 = Yes, 0 = No)", min_value=0, max_value=1, step=1)
skills = st.number_input("Skills Score (0-10)", min_value=0, max_value=10, step=1)

# predict button
if st.button("Predict"):
    input_data = np.array([[cgpa, projects, internship, skills]])
    
    prediction = model.predict(input_data)

    if prediction[0] == 1:
        st.success("🎉 High chance of placement!")
    else:
        st.error("📉 Low chances of placement. Improve skills!")