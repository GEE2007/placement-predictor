import re

import streamlit as st
import joblib
import pandas as pd
from io import BytesIO
from PyPDF2 import PdfReader
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
import plotly.graph_objects as go

def create_pdf_report(resume_score, adjusted_prob, placement_status,
                       cgpa, internships, projects, certifications,
                       aptitude_score, selected_skills, recommendations):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    title_style = ParagraphStyle('Title', parent=styles['Title'],
                                  textColor=colors.HexColor('#2563eb'), fontSize=20)
    story.append(Paragraph("🎯 Placement Readiness Report", title_style))
    story.append(Spacer(1, 12))

    story.append(Paragraph(f"<b>Resume Score:</b> {resume_score}/100", styles['Normal']))
    story.append(Paragraph(f"<b>Placement Probability:</b> {adjusted_prob:.1%}", styles['Normal']))
    story.append(Paragraph(f"<b>Status:</b> {placement_status}", styles['Normal']))
    story.append(Spacer(1, 12))

    data = [["Metric", "Value"],
            ["CGPA", cgpa], ["Internships", internships],
            ["Projects", projects], ["Certifications", certifications],
            ["Aptitude Score", aptitude_score],
            ["Skills", ", ".join(selected_skills) or "None"]]
    
    table = Table(data, colWidths=[200, 250])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f4ff')]),
    ]))
    story.append(table)
    story.append(Spacer(1, 12))

    if recommendations:
        story.append(Paragraph("<b>Recommendations:</b>", styles['Normal']))
        for rec in recommendations:
            story.append(Paragraph(rec, styles['Normal']))

    doc.build(story)
    buffer.seek(0)
    return buffer.read()
    

st.set_page_config(
    page_title="Placement Predictor",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "extracted_cgpa" not in st.session_state:
    st.session_state.extracted_cgpa = None

def load_css():
    with open("stylesheet.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()


def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def extract_cgpa_from_text(text):
    """
    Extract CGPA/GPA from resume text using regex.
    
    Supports formats like:
    - CGPA: 8.5
    - GPA: 3.7
    - CGPA/GPA 8.2
    - 8.5/10
    - GPA 3.7 / 4.0
    
    Returns:
        float or None: Extracted CGPA value (normalized to 10-scale) or None if not found
    """
    if not text:
        return None
    
    text_lower = text.lower()
    
    pattern1 = r'(?:cgpa|gpa)\s*:?\s*(\d+\.?\d*)'
    match1 = re.search(pattern1, text_lower)
    if match1:
        try:
            value = float(match1.group(1))
            if value <= 4.0:
                value = (value / 4.0) * 10
            if 0 <= value <= 10:
                return round(value, 2)
        except ValueError:
            pass

    pattern2 = r'(\d+\.?\d*)\s*/\s*10'
    match2 = re.search(pattern2, text_lower)
    if match2:
        try:
            value = float(match2.group(1))
            if 0 <= value <= 10:
                return round(value, 2)
        except ValueError:
            pass
    
    pattern3 = r'(?:cgpa|gpa)\s*:?\s*(\d+\.?\d*)\s*/\s*4'
    match3 = re.search(pattern3, text_lower)
    if match3:
        try:
            value = float(match3.group(1))
            value = (value / 4.0) * 10
            if 0 <= value <= 10:
                return round(value, 2)
        except ValueError:
            pass
    return None 


def detect_skills_from_text(text, skill_options):
    text_lower = text.lower()
    skill_keywords = {
        "HTML/CSS": ["html", "css"],
        "JavaScript": ["javascript"],
        "React": ["react"],
        "Next.js": ["next.js", "next js"],
        "Tailwind CSS": ["tailwind css", "tailwind"],
        "TypeScript": ["typescript"],
        "Python": ["python"],
        "Java": ["java"],
        "C++": ["c++"],
        "SQL": ["sql"],
        "MongoDB": ["mongodb"],
        "Node.js": ["node.js", "node js"],
        "Express.js": ["express.js", "express js"],
        "Firebase": ["firebase"],
        "Git/GitHub": ["git", "github"],
        "REST APIs": ["rest api", "rest apis", "restful"],
        "DSA": ["dsa", "data structures", "algorithms"],
        "OOP": ["oop", "object oriented programming", "object oriented"],
        "DBMS": ["dbms", "database management system", "database management systems"],
        "Operating Systems": ["operating system", "operating systems"],
        "Computer Networks": ["computer networks", "networking"],
        "Machine Learning": ["machine learning", "ml"],
        "Data Analysis": ["data analysis", "data analytics"],
        "Pandas": ["pandas"],
        "NumPy": ["numpy"],
        "AWS": ["aws"],
        "Docker": ["docker"]
    }

    detected = []
    for skill in skill_options:
        for keyword in skill_keywords.get(skill, [skill.lower()]):
            if re.search(rf"\b{re.escape(keyword)}\b", text_lower):
                detected.append(skill)
                break
    return detected


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
                "Certifications",
                "Aptitude Score"
            ],
            "Max Weight": [
                "10.0",
                "10",
                "10",
                "10",
                "100"
            ],
            "Contribution": [
                "20%",
                "20%",
                "20%",
                "20%",
                "20%"
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
        st.divider()

        st.markdown("### 👨‍💻 Developer")
        st.info(
            "Built to help students evaluate placement readiness using "
            "machine learning, profile analysis, and skill-gap insights."
        )

col_header = st.container()
with col_header:
    st.markdown('<p class="main-header">🎯 Placement Predictor</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Evaluate your profile and estimate placement readiness intelligently', unsafe_allow_html=True)

st.divider()

st.markdown("### 📋 Enter Your Profile Details")

col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown("**Academic Performance**")
    cgpa = st.number_input(
    "CGPA",
    0.0,
    10.0,
    value=float(st.session_state.extracted_cgpa) if st.session_state.extracted_cgpa is not None else 7.0,
    step=0.1,
    help="Cumulative GPA on a scale of 10"
)
    aptitude_score = st.number_input("Aptitude Score", 0.0, 100.0, step=0.1, help="Score out of 100")

with col2:
    st.markdown("**Internships & Projects**")
    internships = st.number_input("Internships", 0, 10, step=1, help="Number of internships completed")
    projects = st.number_input("Projects", 0, 10, step=1, help="Number of projects completed")

with col3:
    st.markdown("**Skills & Certifications**")
    certifications = st.number_input("Certifications", 0, 10, step=1, help="Number of certifications")
    skill_options = [
    "HTML/CSS",
    "JavaScript",
    "React",
    "Next.js",
    "Tailwind CSS",
    "TypeScript",
    "Python",
    "Java",
    "C++",
    "SQL",
    "MongoDB",
    "Node.js",
    "Express.js",
    "Firebase",
    "Git/GitHub",
    "REST APIs",
    "DSA",
    "OOP",
    "DBMS",
    "Operating Systems",
    "Computer Networks",
    "Machine Learning",
    "Data Analysis",
    "Pandas",
    "NumPy",
    "AWS",
    "Docker"
    ]
    resume_file = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"],
        help="Upload your resume to auto-detect skills and CGPA from the PDF"
    )
    detected_skills = []
    if resume_file is not None:
        try:
            resume_text = extract_text_from_pdf(resume_file)
            extracted_cgpa = extract_cgpa_from_text(resume_text)
            st.session_state.extracted_cgpa = extracted_cgpa  
            if extracted_cgpa:
                st.success(f"Detected CGPA: {extracted_cgpa}") 
            detected_skills = detect_skills_from_text(resume_text, skill_options)
            if detected_skills:
                st.markdown("**Detected Skills from Resume:**")
                st.write(", ".join(detected_skills))
            else:
                st.info("No matching skills were detected in the upload.")
        except Exception:
            st.error("Could not extract text from the uploaded PDF. Please upload a valid resume file.")
            st.session_state.extracted_cgpa = None
    selected_skills = st.multiselect(
        "Select Technologies You Know",
        options=skill_options,
        default=detected_skills,
        help="Choose the skills and technologies you have experience with"
    )
    career_goal = st.selectbox(
    "🎯 Target Role",
    [
        "Software Development Engineer (SDE)",
        "Frontend Developer",
        "Backend Developer",
        "Data Analyst",
        "AI/ML Engineer"
    ]
    )   
    skill_count = len(selected_skills)
    skill_score_normalized = min(skill_count / len(skill_options), 1.0)
    skill_score_internal = (skill_count / len(skill_options)) * 100
    required_skills = {
    "Software Development Engineer (SDE)": [
        "DSA",
        "OOP",
        "DBMS",
        "Operating Systems",
        "Java"
    ],

    "Frontend Developer": [
        "HTML/CSS",
        "JavaScript",
        "React",
        "Tailwind CSS"
    ],

    "Backend Developer": [
        "Node.js",
        "Express.js",
        "MongoDB",
        "SQL"
    ],

    "Data Analyst": [
        "Python",
        "SQL",
        "Pandas",
        "Data Analysis"
    ],

    "AI/ML Engineer": [
        "Python",
        "Machine Learning",
        "Pandas",
        "NumPy"
    ]
}
    

    missing_skills = [
    skill for skill in required_skills[career_goal]
    if skill not in selected_skills
    ]

st.divider()

st.markdown("### 📊 Profile Overview")

metric_col1, metric_col2, metric_col3 = st.columns(3, gap="large")

with metric_col1:
    st.metric("CGPA", f"{cgpa:.2f}/10", delta=None)
    st.progress(max(cgpa / 10, 0), text=f"Progress: {(cgpa/10)*100:.0f}%")

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

def calculate_resume_score():
    return (
        (cgpa / 10) * 35 +
        min(internships / 3, 1) * 20 +
        min(projects / 4, 1) * 15 +
        skill_score_normalized * 15 +
        min(certifications / 3, 1) * 5 +
    (aptitude_score / 100) * 10
)

resume_score = round(min(calculate_resume_score(), 100), 1)

score_col1, score_col2 = st.columns([1, 3], gap="large")
with score_col1:
    st.metric("Resume Score", f"{resume_score:.1f}/100", delta=None)
with score_col2:
    st.caption("Calculated from CGPA, internships, projects, certifications, coding effort, and aptitude.")

st.markdown("### 📈 Profile Radar Analysis")

categories = [
    "CGPA",
    "Internships",
    "Projects",
    "Skills",
    "Certifications",
    "Aptitude"
]

values = [
    cgpa / 10 * 100,
    internships / 10 * 100,
    projects / 10 * 100,
    skill_score_normalized * 100,
    certifications / 10 * 100,
    aptitude_score
]

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=values,
    theta=categories,
    fill='toself',
    name='Profile Strength'
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 100]
        )),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("### 🥇 Profile Strength Comparison")
benchmarks = {
    "Average Student": 55,
    "Placement Ready Student": 72,
    "Top Candidate": 88,
}
comparison_cols = st.columns(3, gap="large")
for col, (label, benchmark) in zip(comparison_cols, benchmarks.items()):
    with col:
        st.metric(label, f"{benchmark}/100", delta=f"{resume_score - benchmark:+.1f}")
        st.progress(min(resume_score / 100, 1.0), text=f"Your score: {resume_score:.1f}/100")

if predict_btn:
    input_data = pd.DataFrame([{
        "cgpa": cgpa,
        "internships": internships,
        "projects_count": projects,
        "coding_skills": skill_score_internal,
        "certifications": certifications,
        "aptitude_score": aptitude_score
    }])

    probability = model.predict_proba(input_data)[0][1]


    adjusted_prob = probability

    if internships == 0:
        adjusted_prob -= 0.05
    elif internships >= 2:
        adjusted_prob += 0.02

    if certifications == 0:
        adjusted_prob -= 0.03
    elif certifications >= 2:
        adjusted_prob += 0.02

    if projects < 2:
        adjusted_prob -= 0.03
    elif projects >= 3:
        adjusted_prob += 0.03

    if aptitude_score < 50:
        adjusted_prob -= 0.03
    elif aptitude_score >= 75:
        adjusted_prob += 0.03

    if cgpa >= 8.5:
        adjusted_prob += 0.03
    elif cgpa < 7:
        adjusted_prob -= 0.05

    adjusted_prob = max(0, min(adjusted_prob, 0.88))

    st.toast("Prediction Generated Successfully 🎉")

    st.markdown("### 🎯 Prediction Results")
    
    result_col1, result_col2, result_col3 = st.columns(3, gap="large")
    
    with result_col1:
        st.metric("Placement Readiness Score", f"{adjusted_prob:.1%}")

    with result_col2:
        st.metric("Resume Score", f"{resume_score}/100")
    
    with result_col3:
        if adjusted_prob >= 0.78:
            placement_status = "🔥 Excellent Prospect"
        elif adjusted_prob >= 0.62:
            placement_status = "👍 Competitive Candidate"
        elif adjusted_prob >= 0.45:
            placement_status = "📈 Growing Potential"
        else:
            placement_status = "⚠️ Needs Stronger Profile"
            
        st.metric("Status", placement_status)
    
    st.markdown("**Placement Readiness Score**")
    st.progress(adjusted_prob, text=f"{adjusted_prob:.1%}")
    st.markdown("### 💪 Key Strengths")

    strengths = []

    if cgpa >= 8:
        strengths.append("Strong Academic Performance")

    if internships >= 1:
        strengths.append("Industry Exposure Through Internships")

    if projects >= 3:
        strengths.append("Excellent Practical Project Experience")

    if aptitude_score >= 75:
        strengths.append("Strong Aptitude and Problem Solving")

    if skill_count >= 4:
        strengths.append("Good Technical Skill Set")

    if strengths:
        for strength in strengths:
            st.success(f"✅ {strength}")
    else:
        st.info("Keep building your profile to unlock stronger highlights.")

    st.markdown("### 📌 Why This Score?")

    if cgpa >= 8.5:
        st.write("✅ Strong CGPA significantly boosted your readiness.")

    if internships == 0:
        st.write("⚠️ No internship experience reduced your score.")

    if projects >= 2:
        st.write("✅ Projects improved your practical profile.")

    if certifications == 0:
        st.write("⚠️ Certifications could further strengthen your resume.")

    if aptitude_score >= 75:
        st.write("✅ Strong aptitude performance helped your chances.")

    elif aptitude_score < 60:
        st.write("⚠️ Aptitude needs improvement for placement tests.")
    
    st.markdown("")
    
    if adjusted_prob >= 0.75:
        st.success("🎉 **Excellent! You have a very strong chance of placement!**", icon="✅")
    elif adjusted_prob >= 0.55:
        st.info("👍 **Good! You have a decent chance. Keep improving!**", icon="ℹ️")
    else:
        st.warning("📈 **Work on improving your profile for better chances.**", icon="⚠️")
    
    st.markdown("**💡 Recommendations:**")

    st.markdown("### 🛣️ Personalized Learning Roadmap")

    roadmap = []

    if career_goal == "Software Development Engineer (SDE)":
        roadmap = [
            "📘 Practice DSA daily using LeetCode",
            "⚙️ Learn DBMS, OS, and OOP concepts",
            "🛠️ Build full-stack projects",
            "🚀 Practice coding interview questions"
        ]

    elif career_goal == "Frontend Developer":
        roadmap = [
            "🎨 Master responsive UI design",
            "⚛️ Build React projects",
            "🌐 Learn APIs and deployment",
            "🧩 Create portfolio-quality frontend apps"
        ]

    elif career_goal == "Backend Developer":
        roadmap = [
            "🗄️ Learn databases and SQL",
            "🔗 Build REST APIs using Node.js",
            "🔐 Implement authentication systems",
            "☁️ Learn deployment basics"
        ]

    elif career_goal == "Data Analyst":
        roadmap = [
            "📊 Learn data visualization",
            "🐍 Practice Python and Pandas",
            "🧠 Analyze datasets",
            "📈 Build analytics dashboards"
        ]

    elif career_goal == "AI/ML Engineer":
        roadmap = [
            "🤖 Learn machine learning fundamentals",
            "📚 Build ML projects using scikit-learn",
            "📊 Practice data preprocessing",
            "🚀 Learn model deployment"
        ]

    for step in roadmap:
        st.write(step)

    st.markdown("### 🚀 Recommended Projects")
    project_suggestions = {
        "Software Development Engineer (SDE)": [
            "Build a full-stack internship tracker with user authentication.",
            "Create a coding challenge platform with problem submission and scoring.",
            "Develop a collaborative team task manager using REST APIs."
        ],
        "Frontend Developer": [
            "Design a responsive portfolio website with animations and dark mode.",
            "Build an e-commerce UI using React and Tailwind CSS.",
            "Create an interactive data dashboard with charts and filters."
        ],
        "Backend Developer": [
            "Build a RESTful API for a blogging platform with database support.",
            "Create an authentication service with JWT and role-based access.",
            "Develop a task scheduler API with SQL or MongoDB persistence."
        ],
        "Data Analyst": [
            "Analyze a real dataset and build a visualization dashboard in Streamlit.",
            "Create a sales performance report with Python, Pandas, and SQL.",
            "Build an insights dashboard that includes trend analysis and forecasts."
        ],
        "AI/ML Engineer": [
            "Build a machine learning model for classification using scikit-learn.",
            "Create an image or text classifier and visualize model performance.",
            "Develop an end-to-end pipeline for data preprocessing and model deployment."
        ]
    }

    for project in project_suggestions[career_goal]:
        st.markdown(f"- {project}")

    st.markdown("### 🚨 Skill Gap Analysis")

    role_alignment_message = ""

    if career_goal == "Software Development Engineer (SDE)":

        if (
            "DSA" in selected_skills and
            ("Python" in selected_skills or "Java" in selected_skills) and
            projects >= 2 and
            aptitude_score >= 70
        ):
            role_alignment_message = (
                "💻 Strong alignment toward SDE roles with solid coding and problem-solving foundations."
            )

        elif "Python" in selected_skills or "Java" in selected_skills:
            role_alignment_message = (
                "⚙️ You have programming foundations, but improving DSA and project depth will strengthen SDE readiness."
            )

        else:
            role_alignment_message = (
                "📈 Focus on programming fundamentals, DSA, and development projects for SDE preparation."
            )


    elif career_goal == "Frontend Developer":

        if (
            all(skill in selected_skills for skill in ["HTML/CSS", "JavaScript", "React"]) and
            projects >= 2
        ):
            role_alignment_message = (
                "🎨 Your profile aligns strongly with frontend development roles and modern UI development."
            )

        elif "HTML/CSS" in selected_skills or "JavaScript" in selected_skills:
            role_alignment_message = (
                "🖥️ You have frontend basics, but learning React and building responsive projects will improve readiness."
            )

        else:
            role_alignment_message = (
                "📈 Start with HTML, CSS, and JavaScript fundamentals to build frontend development skills."
            )


    elif career_goal == "Backend Developer":

        if (
            "Python" in selected_skills and
            "SQL" in selected_skills and
            projects >= 2
        ):
            role_alignment_message = (
                "⚙️ Strong backend alignment with database and server-side development foundations."
            )

        elif "Python" in selected_skills or "SQL" in selected_skills:
            role_alignment_message = (
                "🛠️ Your backend foundation is growing, but API development and database skills need improvement."
            )

        else:
            role_alignment_message = (
                "📈 Learn backend programming, databases, and APIs to prepare for backend engineering roles."
            )


    elif career_goal == "Data Analyst":

        if (
            "Python" in selected_skills and
            "SQL" in selected_skills and
            aptitude_score >= 65
        ):
            role_alignment_message = (
                "📊 Your analytical skillset aligns well with data analysis and business intelligence roles."
            )

        elif "SQL" in selected_skills or "Python" in selected_skills:
            role_alignment_message = (
                "📈 You have analytical foundations, but improving data visualization and analytics skills will help."
            )

        else:
            role_alignment_message = (
                "📚 Focus on Python, SQL, and data analysis fundamentals for analyst roles."
            )


    elif career_goal == "AI/ML Engineer":

        if (
            "Python" in selected_skills and
            "Machine Learning" in selected_skills and
            projects >= 2
        ):
            role_alignment_message = (
                "🤖 Strong AI/ML alignment with machine learning foundations and practical exposure."
            )

        elif "Python" in selected_skills or "Machine Learning" in selected_skills:
            role_alignment_message = (
                "🧠 You have some AI/ML foundations, but building ML projects and learning model deployment will help."
            )

        else:
            role_alignment_message = (
                "📈 Start with Python, mathematics, and machine learning fundamentals for AI/ML roles."
            )

    st.info(role_alignment_message)

    if missing_skills:
        st.markdown("#### Missing Skills")
        for skill in missing_skills:
            st.markdown(f"- {skill}")
    else:
        st.success(f"🎉 You already match the core skills for {career_goal}")
    
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
    
    if career_goal == "Software Development Engineer (SDE)":

        if "DSA" not in selected_skills:
            recommendations.append("• Practice DSA regularly for coding interviews")

        if "Python" not in selected_skills and "Java" not in selected_skills:
            recommendations.append("• Learn a programming language like Python or Java")

        if projects < 2:
            recommendations.append("• Build full-stack or problem-solving based projects")

    if career_goal == "Frontend Developer":

        if "JavaScript" not in selected_skills:
            recommendations.append("• Strengthen JavaScript fundamentals for frontend development")

        if "React" not in selected_skills:
            recommendations.append("• Learn React and build responsive frontend projects")

        if projects < 2:
            recommendations.append("• Build responsive UI projects and portfolio websites")

    if career_goal == "Backend Developer":

        if "SQL" not in selected_skills:
            recommendations.append("• Improve backend/database skills using SQL")

        if "Python" not in selected_skills and "Java" not in selected_skills:
            recommendations.append("• Learn a backend programming language like Python or Java")

        if projects < 2:
            recommendations.append("• Build backend API projects using databases and authentication")

    if career_goal == "AI/ML Engineer":

        if "Machine Learning" not in selected_skills:
            recommendations.append("• Build ML projects using scikit-learn and pandas")

        if "Python" not in selected_skills:
            recommendations.append("• Strengthen Python programming for AI/ML development")

        if projects < 2:
            recommendations.append("• Build AI/ML projects to gain practical experience")
    
    if recommendations:
        for rec in recommendations:
            st.write(rec)
    else:
        st.success("✨ Your profile is well-rounded! Keep up the excellent work!")

    clean_status = placement_status.split(" ", 1)[1]

    pdf_bytes = create_pdf_report(
        resume_score=resume_score,
        adjusted_prob=adjusted_prob,
        placement_status=clean_status,
        cgpa=cgpa,
        internships=internships,
        projects=projects,
        certifications=certifications,
        aptitude_score=aptitude_score,
        selected_skills=selected_skills,
        recommendations=recommendations,
    )

    st.download_button(
        label="📄 Download Placement Readiness Report",
        data=pdf_bytes,
        file_name="placement_readiness_report.pdf",
        mime="application/pdf",
        use_container_width=True,
    )
    st.divider()
    st.caption("🚀 Built with Streamlit, Scikit-learn, Plotly & Python")


    