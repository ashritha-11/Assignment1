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
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
    background-color: #0B1120;
    color: white;
}

/* Main Area */
.main .block-container {
    padding-top: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #111827;
    width: 330px !important;
    min-width: 330px !important;
    border-right: 1px solid #1F2937;
}

/* Sidebar Text */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Sidebar Header */
.sidebar-title {
    font-size: 28px;
    font-weight: 700;
    margin-bottom: 20px;
}

/* Main Title */
.main-title {
    font-size: 52px;
    font-weight: 700;
    color: white;
    margin-bottom: 10px;
}

/* Subtitle */
.sub-title {
    font-size: 18px;
    color: #94A3B8;
    margin-bottom: 40px;
}

/* Metric Cards */
.metric-card {
    background: linear-gradient(145deg, #111827, #1E293B);
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    border: 1px solid #334155;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.4);
}

/* Metric Value */
.metric-value {
    font-size: 38px;
    font-weight: 700;
    color: white;
}

/* Metric Label */
.metric-label {
    color: #CBD5E1;
    margin-top: 8px;
    font-size: 16px;
}

/* Result Card */
.result-card {
    background: linear-gradient(145deg, #111827, #1E293B);
    padding: 35px;
    border-radius: 22px;
    border: 1px solid #334155;
    box-shadow: 0px 10px 25px rgba(0,0,0,0.35);
}

/* Button */
.stButton > button {
    width: 100%;
    height: 58px;
    border: none;
    border-radius: 16px;
    background: linear-gradient(to right, #00C853, #00E676);
    color: white;
    font-size: 18px;
    font-weight: 600;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.02);
    background: linear-gradient(to right, #00E676, #00C853);
}

/* Inputs */
.stSlider, .stSelectbox {
    padding-bottom: 10px;
}

/* Hide Streamlit Branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="main-title">
📊 Employee Attrition Predictor
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="sub-title">
AI-Powered Workforce Attrition Analysis Dashboard
</div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("""
    <div class="sidebar-title">
    Employee Details
    </div>
    """, unsafe_allow_html=True)

    age = st.slider(
        "Age",
        18,
        60,
        30
    )

    monthly_income = st.slider(
        "Monthly Income",
        1000,
        50000,
        5000
    )

    job_satisfaction = st.select_slider(
        "Job Satisfaction",
        options=[1, 2, 3, 4],
        value=2
    )

    distance_from_home = st.slider(
        "Distance From Home",
        1,
        50,
        5
    )

    total_working_years = st.slider(
        "Total Working Years",
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
# DASHBOARD CARDS
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">₹ {monthly_income}</div>
        <div class="metric-label">Monthly Income</div>
    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{job_satisfaction}/4</div>
        <div class="metric-label">Job Satisfaction</div>
    </div>
    """, unsafe_allow_html=True)

with col3:

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{total_working_years} Years</div>
        <div class="metric-label">Experience</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# INPUT DATAFRAME
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

    try:

        prediction = model.predict(input_data)[0]

        probability = model.predict_proba(input_data)[0][1] * 100

        if probability >= 70:
            risk = "🔴 HIGH RISK"

        elif probability >= 40:
            risk = "🟠 MEDIUM RISK"

        else:
            risk = "🟢 LOW RISK"

        st.markdown("## Prediction Result")

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

        if prediction == 1:
            st.error("Employee likely to leave the organization.")
        else:
            st.success("Employee likely to stay.")

    except Exception as e:

        st.error(f"Prediction Error: {e}")
