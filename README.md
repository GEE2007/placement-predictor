# 🎯 Placement Predictor

An ML-powered web app that predicts student placement readiness based on academic performance, technical skills, and practical experience — giving actionable insights to help students land their dream role.

---

## 🔗 Live Demo
https://placement-predictor-egdt9dmdzmasdg6zpanwb3.streamlit.app/

## 📌 Overview

Placement Predictor is an end-to-end machine learning web application built with Streamlit that evaluates student placement readiness using academic, technical, and practical profile metrics.

Students can input their profile details, receive placement probability predictions, identify skill gaps, explore suitable career roles, and download a personalized PDF report — all through an interactive dashboard.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔮 Placement Probability | ML-predicted likelihood of getting placed |
| 📄 Resume Readiness Score | Evaluates how job-ready your profile is |
| 🔍 Skill Gap Analysis | Identifies missing skills for your target role |
| 🎯 Role-Based Recommendations | Personalized improvement suggestions |
| 📊 Radar Chart Visualization | Interactive profile strength analysis |
| 📥 PDF Report Generation | Downloadable placement readiness report |
| 🌐 Interactive Dashboard | Clean and responsive Streamlit UI |

---

## 🛠️ Tech Stack

### Frontend & App
- Streamlit — Interactive web dashboard

### Machine Learning
- Scikit-learn — Random Forest Classifier + StandardScaler
- Pandas & NumPy — Data preprocessing and analysis

### Visualization
- Plotly — Interactive radar charts and profile visualization

### Report Generation
- ReportLab — PDF report export functionality

---

## 🤖 ML Model

### Algorithm
- Random Forest Classifier

### Preprocessing
- StandardScaler for feature scaling

### Input Features
- CGPA
- Internships
- Projects
- Certifications
- Technical Skills
- Aptitude Score

### Output
- Placement probability score
- Placement readiness status
- Skill gap insights
- Career recommendations

---

## 🎯 Supported Target Roles

- 💻 Software Development Engineer (SDE)
- 🎨 Frontend Developer
- ⚙️ Backend Developer
- 📈 Data Analyst
- 🤖 AI/ML Engineer

---

## 📁 Project Structure

```bash
placement-predictor/
│
├── app.py
├── train.py
├── model.pkl
├── requirements.txt
├── README.md
│
├── data/
│   └── student_placement.csv
```

---

## ⚙️ Getting Started

### Prerequisites

- Python 3.9 or higher
- pip

---

## 🚀 Run Locally

```bash
git clone https://github.com/GEE2007/placement-predictor.git
cd placement-predictor
pip install -r requirements.txt
streamlit run app.py

The application will open at:

```bash
http://localhost:8501
```

---

## 📦 Requirements

```txt
streamlit
scikit-learn
pandas
numpy
plotly
joblib
PyPDF2
reportlab
```

---

## 🌐 Deployment

This application is deployed using Streamlit Community Cloud.

---

## 📊 Dataset

The model is trained on a synthetic placement dataset containing academic, technical, and practical student profile metrics with corresponding placement outcomes.

Since the dataset is synthetic and relatively small, the model is intended for educational and portfolio purposes rather than real-world hiring decisions.

### Model Accuracy
- ~68% test accuracy on the synthetic dataset

### Features Included
- Academic performance
- Internship experience
- Technical projects
- Certifications
- Technical skills
- Aptitude performance

To retrain the model:

```bash
python train.py
```

---

## 🚀 Future Improvements

- Resume PDF parsing using NLP
- Company-tier prediction
- Personalized learning roadmap generation
- Real placement dataset integration
- Authentication system for students
- Interview preparation recommendations

---



