import streamlit as st
import pandas as pd
import pickle
import warnings

warnings.filterwarnings("ignore")

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Employee Attrition Predictor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# LOAD MODEL
# =========================================================

@st.cache_resource
def load_model():
    return pickle.load(open("random_forest.pkl", "rb"))

model = load_model()

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
    background-color: #0B1120;
    color: white;
}

/* MAIN */
.block-container {
    padding-top: 1.5rem;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background-color: #111827;
    min-width: 320px;
    max-width: 320px;
    border-right: 1px solid #1F2937;
}

/* SIDEBAR TEXT */
[data-testid="stSidebar"] * {
    color: white;
}

/* TITLE */
.main-title {
    font-size: 48px;
    font-weight: 700;
    color: white;
}

.sub-title {
    color: #94A3B8;
    font-size: 18px;
    margin-bottom: 30px;
}

/* CARDS */
.metric-card {
    background: linear-gradient(145deg, #111827, #1E293B);
    padding: 30px;
    border-radius: 22px;
    text-align: center;
    border: 1px solid #334155;
    box-shadow: 0 8px 24px rgba(0,0,0,0.4);
}

.metric-value {
    font-size: 36px;
    font-weight: 700;
}

.metric-label {
    color: #CBD5E1;
    margin-top: 8px;
}

/* RESULT CARD */
.result-card {
    background: linear-gradient(145deg, #111827, #1E293B);
    padding: 30px;
    border-radius: 20px;
    border: 1px solid #334155;
}

/* BUTTON */
.stButton > button {
    width: 100%;
    height: 58px;
    border: none;
    border-radius: 16px;
    background: linear-gradient(to right, #00C853, #00E676);
    color: white;
    font-size: 18px;
    font-weight: 600;
}

.stButton > button:hover {
    background: linear-gradient(to right, #00E676, #00C853);
}

/* HIDE STREAMLIT */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">📊 Employee Attrition Predictor</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">AI Workforce Risk Analysis Dashboard</div>',
    unsafe_allow_html=True
)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("Employee Details")

    age = st.slider("Age", 18, 60, 30)

    monthly_income = st.slider(
        "Monthly Income",
        1000,
        50000,
        5000
    )

    job_satisfaction = st.select_slider(
        "Job Satisfaction",
        options=[1,2,3,4],
        value=2
    )

    distance_from_home = st.slider(
        "Distance From Home",
        1,
        50,
        5
    )

    total_working_years = st.slider(
        "Experience",
        0,
        40,
        5
    )

    years_at_company = st.slider(
        "Years At Company",
        0,
        40,
        3
    )

    overtime = st.selectbox(
        "OverTime",
        ["Yes", "No"]
    )

# =========================================================
# METRICS
# =========================================================

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">₹ {monthly_income}</div>
        <div class="metric-label">Monthly Income</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{job_satisfaction}/4</div>
        <div class="metric-label">Job Satisfaction</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{total_working_years} Years</div>
        <div class="metric-label">Experience</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# INPUT DATA
# =========================================================

overtime = 1 if overtime == "Yes" else 0

input_data = pd.DataFrame([{

    'Age': age,
    'BusinessTravel': 1,
    'DailyRate': 1100,
    'Department': 1,
    'DistanceFromHome': distance_from_home,
    'Education': 3,
    'EducationField': 1,
    'EmployeeCount': 1,
    'EmployeeNumber': 1,
    'EnvironmentSatisfaction': 3,
    'Gender': 1,
    'HourlyRate': 60,
    'JobInvolvement': 3,
    'JobLevel': 2,
    'JobRole': 2,
    'JobSatisfaction': job_satisfaction,
    'MaritalStatus': 1,
    'MonthlyIncome': monthly_income,
    'MonthlyRate': 12000,
    'NumCompaniesWorked': 2,
    'Over18': 1,
    'OverTime': overtime,
    'PercentSalaryHike': 12,
    'PerformanceRating': 3,
    'RelationshipSatisfaction': 3,
    'StandardHours': 80,
    'StockOptionLevel': 1,
    'TotalWorkingYears': total_working_years,
    'TrainingTimesLastYear': 2,
    'WorkLifeBalance': 3,
    'YearsAtCompany': years_at_company,
    'YearsInCurrentRole': 3,
    'YearsSinceLastPromotion': 1,
    'YearsWithCurrManager': 3

}])

# =========================================================
# PREDICTION
# =========================================================

if st.button("Predict Attrition Risk"):

    prediction = model.predict(input_data)[0]

    probability = model.predict_proba(input_data)[0][1] * 100

    if probability >= 70:
        risk = "🔴 HIGH RISK"

    elif probability >= 40:
        risk = "🟠 MEDIUM RISK"

    else:
        risk = "🟢 LOW RISK"

    r1, r2 = st.columns(2)

    with r1:

        st.markdown(f"""
        <div class="result-card">
            <h1>{probability:.2f}%</h1>
            <p>Attrition Probability</p>
        </div>
        """, unsafe_allow_html=True)

        st.progress(int(probability))

    with r2:

        st.markdown(f"""
        <div class="result-card">
            <h1>{risk}</h1>
            <p>Employee Risk Analysis</p>
        </div>
        """, unsafe_allow_html=True)
