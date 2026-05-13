import streamlit as st
import joblib
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="Placement Predictor",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #0066cc;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #0066cc;
    }
    </style>
    """, unsafe_allow_html=True)

model = joblib.load("model.pkl")

col_header = st.container()
with col_header:
    st.markdown('<p class="main-header">🎯 Placement Predictor</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Analyze your profile and predict your placement chances with AI</p>', unsafe_allow_html=True)

st.divider()

st.markdown("### 📋 Enter Your Profile Details")

col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown("**Academic Performance**")
    cgpa = st.number_input("CGPA", 0.0, 10.0, step=0.1, help="Cumulative GPA on a scale of 10")
    aptitude_score = st.number_input("Aptitude Score", 0.0, 100.0, step=0.1, help="Score out of 100")

with col2:
    st.markdown("**Experience & Skills**")
    internships = st.number_input("Internships", 0, 10, step=1, help="Number of internships completed")
    projects = st.number_input("Projects", 0, 10, step=1, help="Number of projects completed")

with col3:
    st.markdown("**Certifications & Coding**")
    certifications = st.number_input("Certifications", 0, 10, step=1, help="Number of certifications")
    leetcode_solved = st.number_input("LeetCode Solved", 0, 1000, step=1, help="Number of problems solved")

st.divider()

st.markdown("### 📊 Profile Overview")

metric_col1, metric_col2, metric_col3 = st.columns(3, gap="large")

with metric_col1:
    st.metric("CGPA", f"{cgpa:.2f}/10", delta=None)
    st.progress(cgpa / 10, text=f"Progress: {(cgpa/10)*100:.0f}%")

with metric_col2:
    st.metric("Internships", f"{internships}/10", delta=None)
    st.progress(internships / 10, text=f"Progress: {(internships/10)*100:.0f}%")

with metric_col3:
    st.metric("Certifications", f"{certifications}/10", delta=None)
    st.progress(certifications / 10, text=f"Progress: {(certifications/10)*100:.0f}%")

metric_col4, metric_col5, metric_col6 = st.columns(3, gap="large")

with metric_col4:
    st.metric("Projects", f"{projects}/10", delta=None)
    st.progress(projects / 10, text=f"Progress: {(projects/10)*100:.0f}%")

with metric_col5:
    st.metric("LeetCode Solved", f"{leetcode_solved}/1000", delta=None)
    st.progress(min(leetcode_solved / 1000, 1.0), text=f"Progress: {min((leetcode_solved/1000)*100, 100):.0f}%")

with metric_col6:
    st.metric("Aptitude Score", f"{aptitude_score:.0f}/100", delta=None)
    st.progress(aptitude_score / 100, text=f"Progress: {aptitude_score:.0f}%")

resume_score = round((
    (cgpa / 10) +
    (internships / 10) +
    (projects / 10) +
    min(leetcode_solved / 1000, 1.0) +
    (certifications / 10)+
    (aptitude_score / 100)
) / 6 * 100, 1)

score_col1, score_col2 = st.columns([1, 3], gap="large")
with score_col1:
    st.metric("Resume Score", f"{resume_score:.1f}/100", delta=None)
with score_col2:
    st.caption("Calculated from CGPA, internships, projects, certifications, coding effort, and aptitude.")

st.markdown("### 📈 Score Comparison")

normalized_data = pd.DataFrame({
    "Metric": [
        "CGPA",
        "Internships",
        "Projects",
        "LeetCode",
        "Certifications",
        "Aptitude Score"
    ],
    "Normalized": [
        cgpa / 10 * 100,
        internships / 10 * 100,
        projects / 10 * 100,
        min(leetcode_solved / 1000 * 100, 100),
        certifications / 10 * 100,
        min(aptitude_score, 100)
    ]
}).set_index("Metric")

st.bar_chart(normalized_data)

st.divider()

col_button = st.columns([1, 4])[0]
with col_button:
    predict_btn = st.button("🚀 Predict Placement", use_container_width=True)

if predict_btn:
    input_data = np.array([[
        cgpa, internships, projects,
        leetcode_solved, certifications, aptitude_score
    ]])

    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)[0][1]

    adjusted_prob = probability

    if aptitude_score < 50:
        adjusted_prob -= 0.10

    if certifications == 0:
        adjusted_prob -= 0.05
    
    if internships == 0:
        adjusted_prob -= 0.15

    if certifications == 0:
        adjusted_prob -= 0.07

    if projects < 2:
        adjusted_prob -= 0.10

    if aptitude_score < 50:
        adjusted_prob -= 0.10

    adjusted_prob = max(0, min(adjusted_prob, .88))

    st.markdown("### 🎯 Prediction Results")
    
    # Result metrics
    result_col1, result_col2, result_col3 = st.columns(3, gap="large")
    
    with result_col1:
        st.metric("Model Probability", f"{probability:.1%}")
    
    with result_col2:
        st.metric("Adjusted Probability", f"{adjusted_prob:.1%}")
    
    with result_col3:
        placement_status = "✅ Strong Chance" if adjusted_prob >= 0.5 else "📈 Needs Improvement"
        st.metric("Status", placement_status)
    
    # Probability visualization
    st.markdown("**Placement Probability Distribution**")
    st.progress(adjusted_prob, text=f"{adjusted_prob:.1%}")
    
    # Result message
    st.markdown("")
    if adjusted_prob >= 0.75:
        st.success("🎉 **Excellent! You have a very strong chance of placement!**", icon="✅")
    elif adjusted_prob >= 0.55:
        st.info("👍 **Good! You have a decent chance. Keep improving!**", icon="ℹ️")
    else:
        st.warning("📈 **Work on improving your profile for better chances.**", icon="⚠️")
    
    st.markdown("**💡 Recommendations:**")
    recommendations = []
    
    if cgpa < 7.0:
        recommendations.append("• Improve your CGPA - aim for 7.0 or higher")
    if internships == 0:
        recommendations.append("• Complete at least 1 internship - highly valued by recruiters")
    if leetcode_solved < 100:
        recommendations.append("• Solve more coding problems on LeetCode to strengthen DSA skills")
    if certifications == 0:
        recommendations.append("• Pursue relevant certifications in your field")
    if aptitude_score < 60:
        recommendations.append("• Work on improving your aptitude score")
    
    if recommendations:
        for rec in recommendations:
            st.write(rec)
    else:
        st.success("✨ Your profile is well-rounded! Keep up the excellent work!")
st.caption("Built with Streamlit, Scikit-learn, Python")


    