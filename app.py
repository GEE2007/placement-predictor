import streamlit as st
import joblib
import numpy as np

model = joblib.load("model.pkl")

st.title("🎯 Placement Predictor")
st.write("Enter your profile details")

cgpa = st.number_input("CGPA", 0.0, 10.0, step=0.1)
projects = st.number_input("Projects Count", 0, 10, step=1)
internships = st.number_input("Internships", 0, 5, step=1)

coding = st.slider("Coding Skills", 1, 10, 5)
dsa = st.slider("DSA Score", 1, 10, 5)
communication = st.slider("Communication Skills", 1, 10, 5)

if st.button("Predict"):
    input_data = np.array([[cgpa, projects, internships, coding, dsa, communication]])

    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)[0][1]

    st.write(f"Placement Probability: {probability:.2%}")

    if prediction[0] == 1:
        st.success("🎉 High chance of placement!")
    else:
        st.error("📉 Lower chance currently. Improve profile!")