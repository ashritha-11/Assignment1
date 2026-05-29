```python
import streamlit as st
import pandas as pd
import numpy as np
import joblib
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
# LOAD FILES
# =========================================================

@st.cache_resource
def load_files():

    model = joblib.load("random_forest.pkl")

    features = joblib.load("features.pkl")

    return model, features

model, features = load_files()

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

.stButton>button {
    width: 100%;
    background: linear-gradient(to right, #4CAF50, #00c853);
    color: white;
    border-radius: 12px;
    height: 3.2em;
    font-size: 18px;
    font-weight: bold;
    border: none;
}

.stButton>button:hover {
    background: linear-gradient(to right, #00c853, #4CAF50);
}

.metric-card {
    background-color: #1E293B;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

st.title("🚀 AI Employee Attrition Prediction System")

st.markdown(
    "Predict employee attrition risk using Machine Learning and HR Analytics."
)

st.markdown("---")

# =========================================================
# SIDEBAR INPUTS
# =========================================================

st.sidebar.header("Employee Information")

age = st.sidebar.slider(
    "Age",
    18,
    60,
    30
)

monthly_income = st.sidebar.number_input(
    "Monthly Income",
    1000,
    50000,
    5000
)

job_satisfaction = st.sidebar.slider(
    "Job Satisfaction",
    1,
    4,
    2
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

overtime = st.sidebar.selectbox(
    "OverTime",
    ["Yes", "No"]
)

gender = st.sidebar.selectbox(
    "Gender",
    ["Male", "Female"]
)

# =========================================================
# ENCODING
# =========================================================

overtime = 1 if overtime == "Yes" else 0

gender = 1 if gender == "Male" else 0

# =========================================================
# DEFAULT VALUES
# =========================================================

default_values = {

    'Age': age,
    'BusinessTravel': 1,
    'DailyRate': 1100,
    'Department': 1,
    'DistanceFromHome': distance_from_home,
    'Education': 3,
    'EducationField': 1,
    'EnvironmentSatisfaction': 3,
    'Gender': gender,
    'HourlyRate': 60,
    'JobInvolvement': 3,
    'JobLevel': 2,
    'JobRole': 2,
    'JobSatisfaction': job_satisfaction,
    'MaritalStatus': 1,
    'MonthlyIncome': monthly_income,
    'MonthlyRate': 12000,
    'NumCompaniesWorked': 2,
    'OverTime': overtime,
    'PercentSalaryHike': 12,
    'PerformanceRating': 3,
    'RelationshipSatisfaction': 3,
    'StockOptionLevel': 1,
    'TotalWorkingYears': total_working_years,
    'TrainingTimesLastYear': 2,
    'WorkLifeBalance': 3,
    'YearsAtCompany': years_at_company,
    'YearsInCurrentRole': 3,
    'YearsSinceLastPromotion': 1,
    'YearsWithCurrManager': 3
}

# =========================================================
# MATCH TRAINING FEATURES
# =========================================================

final_input = {}

for feature in features:

    if feature in default_values:

        final_input[feature] = default_values[feature]

    else:

        final_input[feature] = 0

# =========================================================
# INPUT DATAFRAME
# =========================================================

input_data = pd.DataFrame([final_input])

input_data = input_data[features]

# =========================================================
# DASHBOARD METRICS
# =========================================================

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "Monthly Income",
        f"₹ {monthly_income}"
    )

with c2:

    st.metric(
        "Job Satisfaction",
        job_satisfaction
    )

with c3:

    st.metric(
        "Experience",
        f"{total_working_years} Years"
    )

st.markdown("---")

# =========================================================
# PREDICTION
# =========================================================

if st.button("Predict Attrition"):

    try:

        prediction = model.predict(input_data)[0]

        probability = model.predict_proba(
            input_data
        )[0][1] * 100

        # =================================================
        # RISK LEVEL
        # =================================================

        if probability >= 70:

            risk = "🔴 HIGH RISK"

        elif probability >= 40:

            risk = "🟠 MEDIUM RISK"

        else:

            risk = "🟢 LOW RISK"

        # =================================================
        # RESULTS
        # =================================================

        st.subheader("Prediction Result")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                label="Attrition Probability",
                value=f"{probability:.2f}%"
            )

            st.progress(int(probability))

        with col2:

            st.success(f"Risk Level: {risk}")

            if prediction == 1:

                st.error(
                    "Employee likely to leave."
                )

            else:

                st.info(
                    "Employee likely to stay."
                )

    except Exception as e:

        st.error(f"Prediction Error: {e}")

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    "Built with Streamlit and Random Forest"
)
```
