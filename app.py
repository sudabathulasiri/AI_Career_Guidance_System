import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="AI Career Guidance System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)


 # Enhanced Custom CSS for better styling and user experience
light_css = """
<style>
body {
    background: linear-gradient(120deg, #f0f4f9 0%, #e0e7ff 100%) !important;
}
.main-container {
    background: #fff;
    border-radius: 18px;
    box-shadow: 0 8px 32px 0 rgba(31, 119, 180, 0.15);
    padding: 2.5rem 2rem 2rem 2rem;
    margin: 2rem auto 2rem auto;
    max-width: 900px;
    animation: fadeIn 1.2s;
}
@keyframes fadeIn {
    0% { opacity: 0; transform: translateY(30px); }
    100% { opacity: 1; transform: translateY(0); }
}
.main-header {
    font-size: 2.7rem;
    color: #3a3a7c;
    text-align: center;
    margin-bottom: 1.5rem;
    font-weight: 800;
    letter-spacing: 1px;
    text-shadow: 1px 2px 8px rgba(31,119,180,0.08);
}
.sub-header {
    font-size: 1.3rem;
    color: #2c3e50;
    margin: 1.2rem 0 0.7rem 0;
    font-weight: 600;
}
.career-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1.5rem;
    border-radius: 12px;
    color: white;
    margin: 1rem 0;
    box-shadow: 0 4px 16px rgba(0,0,0,0.10);
    font-size: 1.1rem;
}
.trait-score {
    background: #f8f9fa;
    padding: 0.5rem 1rem;
    border-radius: 7px;
    margin: 0.3rem 0;
    border-left: 5px solid #1f77b4;
    font-size: 1.05rem;
}
.confidence-high { color: #27ae60; font-weight: bold; }
.confidence-medium { color: #f39c12; font-weight: bold; }
.confidence-low { color: #e74c3c; font-weight: bold; }
.badge {
    display: inline-block;
    padding: 0.25em 0.7em;
    font-size: 1em;
    font-weight: 700;
    border-radius: 0.5em;
    margin-left: 0.5em;
    box-shadow: 0 2px 8px rgba(31,119,180,0.08);
}
.badge-green { background: #27ae60; color: white; }
.badge-orange { background: #f39c12; color: white; }
.badge-red { background: #e74c3c; color: white; }
.testimonial {
    background: #f1f8ff;
    border-left: 5px solid #1f77b4;
    margin: 1em 0;
    padding: 1em;
    border-radius: 8px;
    font-style: italic;
    font-size: 1.05rem;
}
.footer {
    text-align: center;
    color: #888;
    font-size: 1rem;
    margin-top: 2.5rem;
    margin-bottom: 0.5rem;
    letter-spacing: 0.5px;
}
</style>
"""
st.markdown(light_css, unsafe_allow_html=True)


# Career database with comprehensive information
CAREER_DATABASE = {
    "Software Engineer": {
        "description": "Design, develop, and maintain software applications and systems using various programming languages and frameworks.",
        "job_roles": ["Full Stack Developer", "Backend Developer", "Mobile App Developer", "DevOps Engineer"],
        "salary_range": "$70,000 - $150,000",
        "tools": ["Python", "JavaScript", "Git", "Docker", "AWS", "React"],
        "required_traits": {"logical_thinking": 0.8, "tech_affinity": 0.9, "math": 0.7, "creativity": 0.6},
        "learning_resources": [
            "IBM SkillsBuild - Software Development",
            "Coursera - Programming Fundamentals",
            "FreeCodeCamp - Web Development"
        ]
    },
    "Data Scientist": {
        "description": "Analyze complex data to extract insights and build predictive models for business decision-making.",
        "job_roles": ["ML Engineer", "Data Analyst", "Business Intelligence Analyst", "Research Scientist"],
        "salary_range": "$80,000 - $160,000",
        "tools": ["Python", "R", "SQL", "Tableau", "TensorFlow", "Jupyter"],
        "required_traits": {"logical_thinking": 0.9, "math": 0.9, "tech_affinity": 0.8, "analytical": 0.8},
        "learning_resources": [
            "IBM Data Science Professional Certificate",
            "Coursera - Data Science Specialization",
            "Kaggle Learn - Data Science"
        ]
    },
    "UX/UI Designer": {
        "description": "Create intuitive and visually appealing user interfaces and experiences for digital products.",
        "job_roles": ["Product Designer", "Visual Designer", "Interaction Designer", "Design Researcher"],
        "salary_range": "$60,000 - $120,000",
        "tools": ["Figma", "Adobe Creative Suite", "Sketch", "InVision", "Principle"],
        "required_traits": {"creativity": 0.9, "empathy": 0.8, "communication": 0.7, "tech_affinity": 0.6},
        "learning_resources": [
            "Google UX Design Certificate",
            "Coursera - UI/UX Design Specialization",
            "Adobe Design University"
        ]
    },
    "Marketing Manager": {
        "description": "Develop and execute marketing strategies to promote products and services to target audiences.",
        "job_roles": ["Digital Marketing Manager", "Brand Manager", "Content Marketing Manager", "Social Media Manager"],
        "salary_range": "$55,000 - $110,000",
        "tools": ["Google Analytics", "HubSpot", "Mailchimp", "Canva", "Hootsuite"],
        "required_traits": {"creativity": 0.8, "communication": 0.9, "leadership": 0.7, "empathy": 0.6},
        "learning_resources": [
            "Google Digital Marketing Certificate",
            "HubSpot Academy",
            "Coursera - Digital Marketing Specialization"
        ]
    },
    "Business Analyst": {
        "description": "Bridge the gap between IT and business by analyzing processes and systems to improve efficiency.",
        "job_roles": ["Systems Analyst", "Process Improvement Analyst", "Data Analyst", "Project Coordinator"],
        "salary_range": "$65,000 - $125,000",
        "tools": ["Excel", "SQL", "Tableau", "JIRA", "Visio", "Power BI"],
        "required_traits": {"logical_thinking": 0.8, "communication": 0.8, "analytical": 0.8, "leadership": 0.6},
        "learning_resources": [
            "IBM Business Analysis Certificate",
            "Coursera - Business Analytics",
            "IIBA - Business Analysis Training"
        ]
    },
    "Project Manager": {
        "description": "Plan, execute, and oversee projects from initiation to completion, ensuring they meet goals and deadlines.",
        "job_roles": ["Scrum Master", "Program Manager", "Operations Manager", "Team Lead"],
        "salary_range": "$70,000 - $130,000",
        "tools": ["Microsoft Project", "JIRA", "Trello", "Slack", "Gantt Charts"],
        "required_traits": {"leadership": 0.9, "communication": 0.8, "organization": 0.8, "problem_solving": 0.7},
        "learning_resources": [
            "PMI Project Management Certificate",
            "Google Project Management Certificate",
            "Coursera - Project Management Principles"
        ]
    },
    "Counselor/Therapist": {
        "description": "Provide mental health support and guidance to individuals dealing with personal challenges.",
        "job_roles": ["Clinical Therapist", "School Counselor", "Career Counselor", "Family Therapist"],
        "salary_range": "$45,000 - $85,000",
        "tools": ["Assessment Tools", "Therapy Software", "Documentation Systems"],
        "required_traits": {"empathy": 0.9, "communication": 0.9, "patience": 0.8, "listening": 0.8},
        "learning_resources": [
            "Psychology Today - Therapy Training",
            "Coursera - Psychology Courses",
            "American Counseling Association Resources"
        ]
    },
    "Sales Representative": {
        "description": "Build relationships with clients and sell products or services to meet revenue targets.",
        "job_roles": ["Account Manager", "Business Development Rep", "Sales Engineer", "Territory Manager"],
        "salary_range": "$45,000 - $120,000",
        "tools": ["CRM Software", "Salesforce", "LinkedIn Sales Navigator", "Email Marketing Tools"],
        "required_traits": {"communication": 0.9, "persuasion": 0.8, "resilience": 0.7, "empathy": 0.6},
        "learning_resources": [
            "Salesforce Trailhead",
            "HubSpot Sales Training",
            "LinkedIn Learning - Sales Skills"
        ]
    }
}

# Quiz questions with trait mapping and tooltips
QUIZ_QUESTIONS = [
    {
        "question": "How comfortable are you with solving complex mathematical problems?",
        "trait": "math",
        "type": "slider",
        "tooltip": "Measures your comfort with numbers, formulas, and quantitative reasoning."
    },
    {
        "question": "Rate your ability to think logically and systematically:",
        "trait": "logical_thinking",
        "type": "slider",
        "tooltip": "Assesses your logical reasoning and structured problem-solving."
    },
    {
        "question": "How much do you enjoy coming up with creative solutions?",
        "trait": "creativity",
        "type": "slider",
        "tooltip": "Reflects your ability to generate new ideas and think outside the box."
    },
    {
        "question": "Rate your comfort level with technology and digital tools:",
        "trait": "tech_affinity",
        "type": "slider",
        "tooltip": "Shows your ease with using computers, software, and digital platforms."
    },
    {
        "question": "How well can you understand and relate to others' emotions?",
        "trait": "empathy",
        "type": "slider",
        "tooltip": "Indicates your ability to empathize and connect with others emotionally."
    },
    {
        "question": "Rate your communication and presentation skills:",
        "trait": "communication",
        "type": "slider",
        "tooltip": "Measures your ability to express ideas clearly and effectively."
    },
    {
        "question": "How comfortable are you taking charge and leading others?",
        "trait": "leadership",
        "type": "slider",
        "tooltip": "Assesses your confidence in guiding and motivating teams."
    },
    {
        "question": "Do you prefer working with data and analysis?",
        "trait": "analytical",
        "type": "radio",
        "options": ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"],
        "tooltip": "Shows your interest in analyzing information and drawing insights."
    },
    {
        "question": "How patient are you when dealing with challenging situations?",
        "trait": "patience",
        "type": "slider",
        "tooltip": "Reflects your ability to remain calm and persistent."
    },
    {
        "question": "Rate your organizational and planning abilities:",
        "trait": "organization",
        "type": "slider",
        "tooltip": "Measures your skill in managing tasks and time efficiently."
    }
]

class CareerGuidanceSystem:
    def __init__(self):
        self.user_data = {}
        self.quiz_scores = {}
        self.ml_model = None
        self.load_or_create_sample_data()
    
    def load_or_create_sample_data(self):
        """Load existing data or create sample dataset for ML model"""
        try:
            self.df = pd.read_csv('career_quiz_data.csv')
        except FileNotFoundError:
            # Create sample dataset
            sample_data = []
            careers = list(CAREER_DATABASE.keys())
            
            for _ in range(100):  # Generate 100 sample records
                record = {}
                career = np.random.choice(careers)
                career_traits = CAREER_DATABASE[career]["required_traits"]
                
                # Generate scores based on career requirements with some noise
                for trait in ["math", "logical_thinking", "creativity", "tech_affinity", 
                             "empathy", "communication", "leadership", "analytical", 
                             "patience", "organization"]:
                    if trait in career_traits:
                        base_score = career_traits[trait]
                        record[trait] = max(1, min(5, np.random.normal(base_score * 5, 0.5)))
                    else:
                        record[trait] = np.random.uniform(1, 5)
                
                record['career'] = career
                sample_data.append(record)
            
            self.df = pd.DataFrame(sample_data)
            self.df.to_csv('career_quiz_data.csv', index=False)
    
    def train_ml_model(self):
        """Train a simple ML model for career prediction"""
        if len(self.df) > 0:
            features = ["math", "logical_thinking", "creativity", "tech_affinity", 
                       "empathy", "communication", "leadership", "analytical", 
                       "patience", "organization"]
            
            X = self.df[features]
            y = self.df['career']
            
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            self.ml_model = RandomForestClassifier(n_estimators=100, random_state=42)
            self.ml_model.fit(X_scaled, y)
            self.scaler = scaler
    
    def calculate_career_match(self, user_scores):
        """Calculate career match using rule-based logic"""
        career_scores = {}
        
        for career, info in CAREER_DATABASE.items():
            required_traits = info["required_traits"]
            total_score = 0
            trait_count = 0
            
            for trait, required_level in required_traits.items():
                if trait in user_scores:
                    user_score = user_scores[trait] / 5.0  # Normalize to 0-1
                    trait_score = 1 - abs(user_score - required_level)
                    total_score += trait_score
                    trait_count += 1
            
            if trait_count > 0:
                career_scores[career] = total_score / trait_count
            else:
                career_scores[career] = 0
        
        return career_scores
    
    def get_personality_tag(self, scores):
        """Generate personality tag based on dominant traits"""
        traits_mapping = {
            "creativity": "Creative Thinker",
            "logical_thinking": "Analytical Mind",
            "empathy": "People Person",
            "leadership": "Natural Leader",
            "tech_affinity": "Tech Enthusiast",
            "communication": "Great Communicator",
            "math": "Problem Solver"
        }
        
        # Find the highest scoring trait
        max_trait = max(scores.keys(), key=lambda x: scores[x])
        return traits_mapping.get(max_trait, "Versatile Professional")
    
    def save_results(self, user_info, career_result, scores):
        """Save results to CSV file"""
        result_data = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'name': user_info.get('name', ''),
            'age': user_info.get('age', ''),
            'education': user_info.get('education', ''),
            'stream': user_info.get('stream', ''),
            'recommended_career': career_result['top_career'],
            'confidence_score': career_result['confidence'],
            'personality_tag': career_result['personality_tag']
        }
        
        # Add scores
        result_data.update(scores)
        
        # Create or append to results file
        results_df = pd.DataFrame([result_data])
        
        if os.path.exists('results.csv'):
            results_df.to_csv('results.csv', mode='a', header=False, index=False)
        else:
            results_df.to_csv('results.csv', index=False)

# Initialize the system
if 'guidance_system' not in st.session_state:
    st.session_state.guidance_system = CareerGuidanceSystem()
    st.session_state.guidance_system.train_ml_model()

# Initialize session state variables
if 'current_step' not in st.session_state:
    st.session_state.current_step = 'landing'
if 'user_info' not in st.session_state:
    st.session_state.user_info = {}
if 'quiz_scores' not in st.session_state:
    st.session_state.quiz_scores = {}

def main():
    # Sidebar with navigation
    st.sidebar.markdown("---")
    st.sidebar.markdown("## 🎯 AI Career Guidance")
    st.sidebar.markdown("### Instructions:")
    st.sidebar.markdown("""
    1. **Fill Personal Info** - Enter your basic details  
    2. **Take the Quiz** - Answer 10 questions honestly  
    3. **Get Recommendations** - View your career matches  
    4. **Explore Careers** - Learn about suggested paths  
    5. **View Analysis** - See your trait visualization  
    """)
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📚 Quick Learning Links")
    st.sidebar.markdown("- [Coursera](https://www.coursera.org/)")
    st.sidebar.markdown("- [Kaggle](https://www.kaggle.com/learn)")
    st.sidebar.markdown("- [FreeCodeCamp](https://www.freecodecamp.org/)")
    st.sidebar.markdown("- [Google Digital Garage](https://learndigital.withgoogle.com/digitalgarage)")
    st.sidebar.markdown("- [LinkedIn Learning](https://www.linkedin.com/learning/)")
    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Start Over"):
        st.session_state.current_step = 'landing'
        st.session_state.user_info = {}
        st.session_state.quiz_scores = {}
        st.rerun()
    # Main header
    st.markdown('<h1 class="main-header">🎯 AI Career Guidance System</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Discover your ideal career path with AI-powered recommendations</p>', unsafe_allow_html=True)
    # Progress bar
    steps = ['landing', 'info', 'quiz', 'results']
    current_step_index = steps.index(st.session_state.current_step)
    progress = (current_step_index + 1) / len(steps)
    st.progress(progress)
    if st.session_state.current_step == 'landing':
        show_landing_page()
    elif st.session_state.current_step == 'info':
        show_user_info_form()
    elif st.session_state.current_step == 'quiz':
        show_quiz()
    elif st.session_state.current_step == 'results':
        show_results()

def show_landing_page():
    st.markdown("""
    <div style="text-align:center;">
        <h2>Welcome to the AI Career Guidance System!</h2>
        <p style="font-size:1.1rem;">
            Take a quick quiz and discover your best-fit career paths, personalized just for you.<br>
            <b>Ready to get started?</b>
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("#### ⭐ What users say:")
    st.markdown('<div class="testimonial">"This tool helped me realize my strengths and choose a career I love!"<br><b>- Priya S.</b></div>', unsafe_allow_html=True)
    st.markdown('<div class="testimonial">"The recommendations were spot-on and the resources are super helpful."<br><b>- Alex T.</b></div>', unsafe_allow_html=True)
    st.markdown('<div class="testimonial">"I loved the visualizations and the easy-to-use interface!"<br><b>- Fatima Z.</b></div>', unsafe_allow_html=True)
    st.markdown("---")
    if st.button("🚀 Start Career Quiz"):
        st.session_state.current_step = 'info'
        st.rerun()

def show_user_info_form():
    st.markdown('<h2 class="sub-header">👤 Personal Information</h2>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", placeholder="Enter your full name")
        age = st.number_input("Age", min_value=15, max_value=65, value=22)
    with col2:
        education = st.selectbox("Education Level", 
                               ["High School", "Bachelor's Degree", "Master's Degree", "PhD", "Other"])
        stream = st.selectbox("Field of Study", 
                            ["Computer Science", "Engineering", "Business", "Arts", "Science", 
                             "Medicine", "Law", "Education", "Other"])
    if st.button("Continue to Quiz ➡️", type="primary"):
        if name:
            st.session_state.user_info = {
                'name': name,
                'age': age,
                'education': education,
                'stream': stream
            }
            st.session_state.current_step = 'quiz'
            st.success("Information saved! Let's start the quiz.")
            st.rerun()
        else:
            st.error("Please enter your name to continue.")

def show_quiz():
    st.markdown('<h2 class="sub-header">📋 Career Assessment Quiz</h2>', unsafe_allow_html=True)
    st.markdown("Rate each statement based on how well it describes you (1 = Strongly Disagree, 5 = Strongly Agree)")
    scores = {}
    with st.form("career_quiz"):
        for i, q in enumerate(QUIZ_QUESTIONS):
            st.markdown(f"**Question {i+1}: {q['question']}** <span title='{q.get('tooltip','')}' style='color:#888;cursor:help;'>ℹ️</span>", unsafe_allow_html=True)
            if q['type'] == 'slider':
                score = st.slider(
                    f"Q{i+1}",
                    min_value=1,
                    max_value=5,
                    value=3,
                    key=f"q_{i}",
                    label_visibility="collapsed"
                )
            else:  # radio
                options = q['options']
                selection = st.radio(
                    f"Q{i+1}",
                    options,
                    key=f"q_{i}",
                    label_visibility="collapsed"
                )
                score = options.index(selection) + 1
            scores[q['trait']] = score
            st.markdown("---")
        submitted = st.form_submit_button("Get My Career Recommendations 🎯", type="primary")
        if submitted:
            st.session_state.quiz_scores = scores
            st.session_state.current_step = 'results'
            st.toast("Quiz completed! Generating your personalized career recommendations...", icon="🎉")
            st.balloons()
            st.rerun()

def show_results():
    st.markdown('<h2 class="sub-header">🧠 Your Career Recommendations</h2>', unsafe_allow_html=True)
    # Calculate career matches
    career_scores = st.session_state.guidance_system.calculate_career_match(st.session_state.quiz_scores)
    sorted_careers = sorted(career_scores.items(), key=lambda x: x[1], reverse=True)
    # Get top 3 recommendations
    top_career = sorted_careers[0][0]
    alternatives = [career[0] for career in sorted_careers[1:3]]
    # Calculate confidence score
    confidence = sorted_careers[0][1] * 100
    # Get personality tag
    personality_tag = st.session_state.guidance_system.get_personality_tag(st.session_state.quiz_scores)
    # Prepare result data
    career_result = {
        'top_career': top_career,
        'alternatives': alternatives,
        'confidence': confidence,
        'personality_tag': personality_tag
    }
    # Display results
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        badge = "badge-green" if confidence > 80 else "badge-orange" if confidence > 60 else "badge-red"
        st.markdown(f"### 🎯 **{top_career}** <span class='badge {badge}'>{confidence:.1f}% match</span>", unsafe_allow_html=True)
    with col2:
        st.metric("Personality Type", personality_tag)
    with col3:
        if st.button("💾 Save Results"):
            st.session_state.guidance_system.save_results(
                st.session_state.user_info, 
                career_result, 
                st.session_state.quiz_scores
            )
            st.success("Results saved!")
        csv = pd.DataFrame([st.session_state.user_info | st.session_state.quiz_scores | career_result]).to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download Results", csv, "career_results.csv", "text/csv")
    # Career details
    show_career_details(top_career, "🏆 Top Recommendation")
    st.markdown("### 🔄 Alternative Career Paths")
    col1, col2 = st.columns(2)
    with col1:
        if len(alternatives) > 0:
            show_career_details(alternatives[0], "🥈 Second Choice", compact=True)
    with col2:
        if len(alternatives) > 1:
            show_career_details(alternatives[1], "🥉 Third Choice", compact=True)
    # Trait analysis
    show_trait_analysis(top_career)
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Retake Quiz", type="secondary"):
            st.session_state.current_step = 'quiz'
            st.rerun()
    with col2:
        if st.button("👤 Update Info", type="secondary"):
            st.session_state.current_step = 'info'
            st.rerun()

def show_career_details(career_name, title, compact=False):
    career_info = CAREER_DATABASE[career_name]
    if not compact:
        st.markdown(f"#### {title}")
        with st.expander(f"Learn more about {career_name}", expanded=True):
            st.markdown(f"**Description:** {career_info['description']}")
            st.markdown(f"**Job Roles:** {', '.join(career_info['job_roles'])}")
            st.markdown(f"**Salary Range:** {career_info['salary_range']}")
            st.markdown(f"**Tools & Technologies:** {', '.join(career_info['tools'])}")
            st.markdown("**Learning Resources:**")
            for resource in career_info['learning_resources']:
                st.markdown(f"• {resource}")
    else:
        with st.expander(f"{career_name}"):
            st.markdown(f"{career_info['description'][:100]}...")
            st.markdown(f"**Salary:** {career_info['salary_range']}")

def show_trait_analysis(top_career=None):
    st.markdown("### 📊 Your Trait Analysis")
    traits = list(st.session_state.quiz_scores.keys())
    scores = list(st.session_state.quiz_scores.values())
    # Radar chart using Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=scores + [scores[0]],  # Close the polygon
        theta=traits + [traits[0]],
        fill='toself',
        name='Your Scores',
        line_color='rgb(31, 119, 180)'
    ))
    # If top_career is provided, show average required traits for comparison
    if top_career:
        required = CAREER_DATABASE[top_career]["required_traits"]
        avg_required = [required.get(trait, 0.5) * 5 for trait in traits]
        fig.add_trace(go.Scatterpolar(
            r=avg_required + [avg_required[0]],
            theta=traits + [traits[0]],
            fill='toself',
            name=f"{top_career} Ideal",
            line_color='rgb(255, 127, 14)'
        ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )),
        showlegend=True,
        title="Your Trait Profile",
        height=500
    )
    col1, col2 = st.columns([2, 1])
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("#### Trait Breakdown")
        for trait, score in st.session_state.quiz_scores.items():
            trait_name = trait.replace('_', ' ').title()
            st.markdown(f'<div class="trait-score">{trait_name}: {score}/5</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()