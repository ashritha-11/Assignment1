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

/* Main Container */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 100%;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid #1F2937;
}

/* Hide Streamlit Branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Header */
.title {
    font-size: 52px;
    font-weight: 700;
    color: white;
    margin-bottom: 0px;
}

.subtitle {
    font-size: 18px;
    color: #94A3B8;
    margin-top: -10px;
    margin-bottom: 30px;
}

/* Metric Cards */
.metric-card {
    background: linear-gradient(145deg, #111827, #1E293B);
    padding: 30px 20px;
    border-radius: 22px;
    text-align: center;
    border: 1px solid #334155;
    box-shadow: 0 8px 25px rgba(0,0,0,0.35);
    transition: 0.3s;
}

.metric-card:hover {
    transform: translateY(-4px);
}

.metric-value {
    font-size: 38px;
    font-weight: 700;
    color: white;
}

.metric-label {
    font-size: 16px;
    color: #CBD5E1;
    margin-top: 8px;
}

/* Prediction Card */
.result-card {
    background: linear-gradient(145deg, #111827, #1E293B);
    padding: 35px;
    border-radius: 24px;
    border: 1px solid #334155;
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
}

/* Button */
.stButton > button {
    width: 100%;
    height: 58px;
    border: none;
    border-radius: 16px;
    background: linear-gradient(to right, #00C853, #00E676);
    color: white;
    font-size: 19px;
    font-weight: 600;
    margin-top: 10px;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.02);
    background: linear-gradient(to right, #00E676, #00C853);
}

/* Inputs */
div[data-baseweb="select"] > div,
.stSlider,
.stNumberInput {
    background-color: #1E293B !important;
    border-radius: 12px;
}

/* Progress */
.stProgress > div > div > div {
    background-color: #00E676;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="title">📊 Employee Attrition Predictor</div>
<div class="subtitle">
AI-Powered Workforce Risk Analysis Dashboard
</div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR INPUTS
# =========================================================

st.sidebar.title("Employee Details")

age = st.sidebar.slider("Age", 18, 60, 30)

monthly_income = st.sidebar.slider(
    "Monthly Income",
    1000,
    50000,
    5000
)

job_satisfaction = st.sidebar.select_slider(
    "Job Satisfaction",
    options=[1, 2, 3, 4],
    value=2
)

distance_from_home = st.sidebar.slider(
    "Distance From Home",
    1,
    50,
    5
)

total_working_years = st.sidebar.slider(
    "Total Working Years",
    0,
    40,
    5
)

years_at_company = st.sidebar.slider(
    "Years At Company",
    0,
    40,
    3
)

job_involvement = st.sidebar.select_slider(
    "Job Involvement",
    options=[1, 2, 3, 4],
    value=3
)

work_life_balance = st.sidebar.select_slider(
    "Work Life Balance",
    options=[1, 2, 3, 4],
    value=3
)

overtime = st.sidebar.selectbox(
    "OverTime",
    ["Yes", "No"]
)

gender = st.sidebar.selectbox(
    "Gender",
    ["Male", "Female"]
)

marital_status = st.sidebar.selectbox(
    "Marital Status",
    ["Single", "Married", "Divorced"]
)

# =========================================================
# ENCODING
# =========================================================

overtime = 1 if overtime == "Yes" else 0
gender = 1 if gender == "Male" else 0

marital_mapping = {
    "Single": 2,
    "Married": 1,
    "Divorced": 0
}

marital_status = marital_mapping[marital_status]

# =========================================================
# INPUT DATAFRAME
# =========================================================

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
    'Gender': gender,
    'HourlyRate': 60,
    'JobInvolvement': job_involvement,
    'JobLevel': 2,
    'JobRole': 2,
    'JobSatisfaction': job_satisfaction,
    'MaritalStatus': marital_status,
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
    'WorkLifeBalance': work_life_balance,
    'YearsAtCompany': years_at_company,
    'YearsInCurrentRole': 3,
    'YearsSinceLastPromotion': 1,
    'YearsWithCurrManager': 3

}])

# =========================================================
# TOP METRICS
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
# PREDICT BUTTON
# =========================================================

if st.button("Predict Attrition Risk"):

    try:

        prediction = model.predict(input_data)[0]

        probability = model.predict_proba(input_data)[0][1] * 100

        # =================================================
        # RISK LEVEL
        # =================================================

        if probability >= 70:
            risk = "🔴 HIGH RISK"
            status = "Employee likely to leave"

        elif probability >= 40:
            risk = "🟠 MEDIUM RISK"
            status = "Employee retention required"

        else:
            risk = "🟢 LOW RISK"
            status = "Employee likely to stay"

        # =================================================
        # RESULTS
        # =================================================

        st.markdown("## Prediction Result")

        r1, r2 = st.columns([1.2, 1])

        with r1:

            st.markdown(f"""
            <div class="result-card">
                <h2 style="font-size:38px; color:white;">
                    {probability:.2f}%
                </h2>
                <p style="font-size:18px; color:#CBD5E1;">
                    Attrition Probability
                </p>
            </div>
            """, unsafe_allow_html=True)

            st.progress(int(probability))

        with r2:

            st.markdown(f"""
            <div class="result-card">
                <h2 style="font-size:34px;">
                    {risk}
                </h2>

                <p style="font-size:18px; color:#CBD5E1;">
                    {status}
                </p>
            </div>
            """, unsafe_allow_html=True)

    except Exception as e:

        st.error(f"Prediction Error: {e}")
