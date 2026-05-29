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

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');

html, body, [class*="css"]  {
    font-family: 'Poppins', sans-serif;
    background-color: #0E1117;
    color: white;
}

/* Main */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid #1F2937;
}

/* Title */
.main-title {
    font-size: 42px;
    font-weight: 700;
    color: white;
    margin-bottom: 5px;
}

.sub-title {
    color: #9CA3AF;
    font-size: 16px;
    margin-bottom: 30px;
}

/* Cards */
.card {
    background: linear-gradient(145deg, #161B22, #1C2333);
    padding: 25px;
    border-radius: 18px;
    border: 1px solid #2D3748;
    box-shadow: 0px 4px 25px rgba(0,0,0,0.35);
}

/* Metric Cards */
.metric-card {
    background: linear-gradient(145deg, #161B22, #1F2937);
    padding: 18px;
    border-radius: 18px;
    text-align: center;
    border: 1px solid #2D3748;
    box-shadow: 0px 0px 15px rgba(0,0,0,0.25);
}

/* Buttons */
.stButton > button {
    width: 100%;
    height: 55px;
    border: none;
    border-radius: 14px;
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
div[data-baseweb="select"] > div,
.stSlider,
.stNumberInput,
.stTextInput {
    background-color: #1F2937 !important;
    border-radius: 10px;
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

st.markdown(
    '<div class="main-title">📊 Employee Attrition Predictor</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">AI-based workforce attrition risk analysis</div>',
    unsafe_allow_html=True
)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("## Employee Details")

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
    "Experience",
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
# INPUT DATA
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
# DASHBOARD CARDS
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>₹ {monthly_income}</h3>
        <p>Monthly Income</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <h3>{job_satisfaction}/4</h3>
        <p>Job Satisfaction</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <h3>{total_working_years} Years</h3>
        <p>Experience</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# PREDICTION
# =========================================================

if st.button("Predict Attrition Risk"):

    try:

        prediction = model.predict(input_data)[0]

        probability = model.predict_proba(input_data)[0][1] * 100

        # ==============================================
        # RISK LEVEL
        # ==============================================

        if probability >= 70:
            risk = "🔴 HIGH RISK"

        elif probability >= 40:
            risk = "🟠 MEDIUM RISK"

        else:
            risk = "🟢 LOW RISK"

        # ==============================================
        # RESULTS
        # ==============================================

        st.markdown("## Prediction Result")

        r1, r2 = st.columns(2)

        with r1:

            st.metric(
                "Attrition Probability",
                f"{probability:.2f}%"
            )

            st.progress(int(probability))

        with r2:

            st.markdown(f"""
            <div class="card">
                <h2>{risk}</h2>
                <p>Employee Risk Analysis</p>
            </div>
            """, unsafe_allow_html=True)

        if prediction == 1:
            st.error("Employee likely to leave the organization.")
        else:
            st.success("Employee likely to stay.")

    except Exception as e:

        st.error(f"Prediction Error: {e}")
