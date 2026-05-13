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
    :root {
        --bg: #eff3fb;
        --panel: #ffffff;
        --panel-soft: #f7f9fc;
        --text: #111827;
        --muted: #54678f;
        --primary: #2563eb;
        --primary-soft: #e5efff;
        --border: rgba(37, 99, 235, 0.18);
    }

    body, .stApp, [data-testid="stAppViewContainer"] {
        background: var(--bg);
        color: var(--text);
    }

    [data-testid="stSidebar"] {
        background: var(--panel);
        border-right: 1px solid rgba(15, 23, 42, 0.08);
        box-shadow: 2px 0 24px rgba(15, 23, 42, 0.06);
    }

    .main-header {
        font-size: 2.6rem;
        font-weight: 700;
        color: var(--primary);
        margin-bottom: 0.25rem;
    }

    .sub-header {
        font-size: 1.05rem;
        color: #1e293b;
        margin-bottom: 2rem;
        line-height: 1.6;
    }

    .css-1d391kg, .css-18e3th9, .css-1v0mbdj, .css-10trblm {
        background: transparent;
    }

    .stMarkdown, .stText, .stCaption {
        color: var(--text);
    }

    .metric-card {
        background: var(--panel);
        padding: 1.2rem;
        border-radius: 1rem;
        border: 1px solid var(--border);
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.04);
    }

    .stButton>button {
        background: var(--primary);
        color: white;
        border: none;
        border-radius: 0.85rem;
        padding: 0.9rem 1.2rem;
        font-size: 1rem;
        font-weight: 600;
        box-shadow: 0 12px 24px rgba(37, 99, 235, 0.16);
    }

    .stButton>button:hover {
        background: #1d4ed8;
    }

    .stProgress .st-bo {
        border-radius: 999px;
        background: var(--panel-soft);
    }

    .stProgress>div>div>div {
        border-radius: 999px;
        background: linear-gradient(90deg, #2563eb 0%, #60a5fa 100%);
    }

    [data-testid="stMetricValue"] {
        font-size: 1.45rem;
        font-weight: 700;
        color: var(--text);
    }

    [data-testid="stMetricDelta"] {
        color: var(--muted);
    }

    .st-expander {
        border: 1px solid rgba(15, 23, 42, 0.08);
        border-radius: 1rem;
        background: var(--panel-soft);
    }

    .st-expander header {
        font-weight: 600;
        color: var(--text);
    }

    .st-dataframe {
        border: 1px solid rgba(15, 23, 42, 0.08);
        border-radius: 1rem;
        background: var(--panel);
    }
    /* All labels like CGPA, Projects etc */
    /* Outside labels like CGPA, Projects */
label[data-testid="stWidgetLabel"] p,
label[data-testid="stWidgetLabel"] span,
label[data-testid="stWidgetLabel"] div {
    color: #111827 !important;
    font-weight: 600 !important;
}

/* Input boxes background dark */
input, textarea {
    background-color: #111827 !important;
    color: white !important;
    border-radius: 8px !important;
}

/* Number input arrows area */
[data-baseweb="input"] {
    background-color: #111827 !important;
    color: white !important;
}

/* Multiselect main box */
[data-baseweb="select"] {
    background-color: #111827 !important;
    color: white !important;
}

/* Selected skill tags */
[data-baseweb="tag"] {
    background-color: #2563eb !important;
    color: white !important;
}

/* Dropdown menu options */
ul[role="listbox"] li {
    background-color: #111827 !important;
    color: white !important;
}

/* Placeholder text */
input::placeholder {
    color: #cbd5e1 !important;
}
/* Metric titles like CGPA, Projects */
[data-testid="stMetricLabel"] {
    color: #111827 !important;
    font-weight: 600 !important;
}

/* Small faded metric label fix */
[data-testid="stMetricLabel"] * {
    color: #111827 !important;
}

/* Resume score caption text */
.stCaption, .stMarkdown p {
    color: #374151 !important;
}
    </style>
    """, unsafe_allow_html=True)

model = joblib.load("model.pkl")




with st.sidebar:
    st.markdown("### 📚 How Scores Are Calculated")
    
    with st.expander("📋 Resume Score", expanded=True):
        st.markdown("""
        **Resume Score** measures your overall profile strength on a scale of 0-100.
        
        **Components:**
        """)
        
        resume_components = pd.DataFrame({
            "Metric": [
                "CGPA",
                "Internships",
                "Projects",
                "LeetCode Problems",
                "Certifications",
                "Aptitude Score"
            ],
            "Max Weight": [
                "10.0",
                "10",
                "10",
                "1000",
                "10",
                "100"
            ],
            "Contribution": [
                "16.7%",
                "16.7%",
                "16.7%",
                "16.7%",
                "16.7%",
                "16.7%"
            ]
        })
        st.dataframe(resume_components, use_container_width=True, hide_index=True)
        
        st.markdown("""
        **Formula:** Average of all normalized components × 100
        
        Each metric is normalized to a 0-1 scale, then averaged and converted to 0-100.
        """)
    
    with st.expander("🎯 Placement Readiness Score"):
        st.markdown("""
        **Placement Readiness Score** (0-88%) predicts your chances of successful placement 
        using machine learning and real-world adjustment factors.
        
        **Calculation Process:**
        1. **Base Probability** - Generated by trained ML model
        2. **Adjustments** - Penalties based on critical gaps:
           - **-10%** if Aptitude Score < 50
           - **-15%** if No Internships
           - **-10%** if Projects < 2
           - **-5%** if No Certifications
        3. **Final Score** - Capped between 0-88%
        
        **Interpretation:**
        - **75%+** 🎉 Excellent placement chances
        - **55-74%** 👍 Good chances, keep improving
        - **<55%** 📈 Focus on profile improvements
        """)
    
    st.divider()
    
    with st.expander("💡 Tips for Improving Your Profile", expanded=True):
        st.markdown("""
        **Quick Wins (1-3 months):**
        - 🎯 Improve Aptitude Score: Practice reasoning & quantitative skills daily
        - 💻 Solve LeetCode Problems: Aim for 50-100 problems to strengthen DSA
        - 📜 Obtain a Certification: Cloud (AWS/GCP), Web Development, or Data Science
        
        **Medium-term Goals (3-6 months):**
        - 🏢 Complete an Internship: 3-6 month duration shows commitment
        - 🛠️ Build 2-3 Projects: Create full-stack applications with real-world problem-solving
        - 📚 Boost CGPA: Target 7.0+ through consistent effort
        
        **Long-term Strategy (6+ months):**
        - 🌟 Develop Specialized Skills: Machine Learning, Cloud, or Full-Stack
        - 🤝 Gain Leadership Experience: Open-source contributions or technical clubs
        - 💼 Network with Professionals: Attend tech meetups and LinkedIn engagement
        
        **Priority Actions:**
        1. If CGPA < 7.0: Focus on academics first
        2. If No Internships: This is a major factor - prioritize immediately
        3. If Low Projects: Build real-world applications
        4. If Low Aptitude: Practice daily for 30-45 minutes
        """)
    
    st.divider()
    
    with st.expander("❓ FAQs"):
        st.markdown("""
        **Q: What's the minimum score to get placed?**
        A: While there's no hard cutoff, scores 60%+ indicate strong placement chances.
        
        **Q: How often is the prediction model updated?**
        A: The model is trained on historical placement data and updated periodically.
        
        **Q: Does aptitude score matter the most?**
        A: All factors matter, but aptitude is a strong indicator for interviews.
        
        **Q: Can I improve my CGPA if it's low?**
        A: Yes! Focus on upcoming semesters. Recent improvements are valued by recruiters.
        
        **Q: What if I don't have an internship?**
        A: Complete one ASAP. It significantly impacts placement chances.
        """)

col_header = st.container()
with col_header:
    st.markdown('<p class="main-header">🎯 Placement Predictor</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Evaluate your profile and estimate placement readiness intelligently', unsafe_allow_html=True)

st.divider()

st.markdown("### 📋 Enter Your Profile Details")

col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown("**Academic Performance**")
    cgpa = st.number_input("CGPA", 0.0, 10.0, step=0.1, help="Cumulative GPA on a scale of 10")
    aptitude_score = st.number_input("Aptitude Score", 0.0, 100.0, step=0.1, help="Score out of 100")

with col2:
    st.markdown("**Internships & Projects**")
    internships = st.number_input("Internships", 0, 10, step=1, help="Number of internships completed")
    projects = st.number_input("Projects", 0, 10, step=1, help="Number of projects completed")

with col3:
    st.markdown("**Skills & Certifications**")
    certifications = st.number_input("Certifications", 0, 10, step=1, help="Number of certifications")
    skill_options = ["HTML/CSS", "JavaScript", "React", "Python", "Java", "SQL", "DSA", "ML"]
    selected_skills = st.multiselect(
        "Select Technologies You Know",
        options=skill_options,
        help="Choose the skills and technologies you have experience with"
    )
    skill_count = len(selected_skills)
    skill_score_normalized = min(skill_count / len(skill_options), 1.0)
    skill_score_internal = skill_count * 125

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
    st.metric("Skills", f"{skill_count}/{len(skill_options)}", delta=None)
    st.progress(skill_score_normalized, text=f"Progress: {skill_score_normalized*100:.0f}%")

with metric_col6:
    st.metric("Aptitude Score", f"{aptitude_score:.0f}/100", delta=None)
    st.progress(aptitude_score / 100, text=f"Progress: {aptitude_score:.0f}%")

resume_score = round((
    (cgpa / 10) +
    (internships / 10) +
    (projects / 10) +
    skill_score_normalized +
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
        "Skills",
        "Certifications",
        "Aptitude Score"
    ],
    "Normalized": [
        cgpa / 10 * 100,
        internships / 10 * 100,
        projects / 10 * 100,
        skill_score_normalized * 100,
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
        skill_score_internal, certifications, aptitude_score
    ]])

    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)[0][1]


    adjusted_prob = probability

    if internships == 0:
        adjusted_prob -= 0.15

    if certifications == 0:
        adjusted_prob -= 0.07

    if projects < 2:
        adjusted_prob -= 0.10

    if aptitude_score < 50:
        adjusted_prob -= 0.10

    adjusted_prob = max(0, min(adjusted_prob, 0.88))

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
    st.markdown("**Placement Readiness Score**")
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
    if skill_count < 3:
        recommendations.append("• Add more relevant skills to your profile and practice them regularly")
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


    