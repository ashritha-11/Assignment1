
import streamlit as st
import pandas as pd
import pickle

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Employee Attrition Predictor",
    page_icon="📊",
    layout="wide"
)

# =========================
# LOAD MODEL
# =========================

model = pickle.load(open("random_forest.pkl", "rb"))

# =========================
# TITLE
# =========================

st.title("🚀 AI Employee Attrition Prediction System")

st.markdown(
    "Predict employee attrition risk using Machine Learning."
)

# =========================
# SIDEBAR INPUTS
# =========================

st.sidebar.header("Employee Information")

age = st.sidebar.slider("Age", 18, 60, 30)

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

# =========================
# ENCODING
# =========================

overtime = 1 if overtime == "Yes" else 0

gender = 1 if gender == "Male" else 0

# =========================
# INPUT DATAFRAME
# =========================

input_data = pd.DataFrame({

    'Age': [age],
    'BusinessTravel': [1],
    'DailyRate': [1100],
    'Department': [1],
    'DistanceFromHome': [distance_from_home],
    'Education': [3],
    'EducationField': [1],
    'EnvironmentSatisfaction': [3],
    'Gender': [gender],
    'HourlyRate': [60],
    'JobInvolvement': [3],
    'JobLevel': [2],
    'JobRole': [2],
    'JobSatisfaction': [job_satisfaction],
    'MaritalStatus': [1],
    'MonthlyIncome': [monthly_income],
    'MonthlyRate': [12000],
    'NumCompaniesWorked': [2],
    'OverTime': [overtime],
    'PercentSalaryHike': [12],
    'PerformanceRating': [3],
    'RelationshipSatisfaction': [3],
    'StockOptionLevel': [1],
    'TotalWorkingYears': [total_working_years],
    'TrainingTimesLastYear': [2],
    'WorkLifeBalance': [3],
    'YearsAtCompany': [years_at_company],
    'YearsInCurrentRole': [3],
    'YearsSinceLastPromotion': [1],
    'YearsWithCurrManager': [3]
})

# =========================
# PREDICTION BUTTON
# =========================

if st.button("Predict Attrition"):

    prediction = model.predict(input_data)[0]

    probability = model.predict_proba(input_data)[0][1] * 100

    if probability >= 70:
        risk = "🔴 HIGH RISK"

    elif probability >= 40:
        risk = "🟠 MEDIUM RISK"

    else:
        risk = "🟢 LOW RISK"

    st.subheader("Prediction Result")

    st.metric(
        label="Attrition Probability",
        value=f"{probability:.2f}%"
    )

    st.success(f"Risk Level: {risk}")

    if prediction == 1:
        st.error("Employee likely to leave.")
    else:
        st.info("Employee likely to stay.")

st.markdown("---")

st.markdown("Built with Streamlit and Random Forest")

