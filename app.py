
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import warnings

warnings.filterwarnings("ignore")

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Employee Attrition Predictor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

h1, h2, h3 {
    color: white;
}

.stButton>button {
    width: 100%;
    background: linear-gradient(to right, #4CAF50, #45a049);
    color: white;
    border-radius: 10px;
    height: 3em;
    font-size: 18px;
    font-weight: bold;
    border: none;
}

.stButton>button:hover {
    background: linear-gradient(to right, #45a049, #4CAF50);
    color: white;
}

.metric-card {
    background-color: #1E1E1E;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0px 0px 10px rgba(0,0,0,0.5);
}

.sidebar .sidebar-content {
    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD MODEL
# =========================================================

@st.cache_resource
def load_model():
    model = pickle.load(open("random_forest.pkl", "rb"))
    return model

model = load_model()

# =========================================================
# HEADER
# =========================================================

st.markdown("""
# 🚀 AI-Powered Employee Attrition Prediction System
""")

st.markdown("""
### Predict employee attrition risk using Machine Learning and HR Analytics
""")

st.markdown("---")

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
    width=120
)

st.sidebar.title("Employee Details")

# =========================================================
# USER INPUTS
# =========================================================

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
# MAIN DASHBOARD
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Monthly Income",
        value=f"₹ {monthly_income}"
    )

with col2:
    st.metric(
        label="Job Satisfaction",
        value=job_satisfaction
    )

with col3:
    st.metric(
        label="Work Experience",
        value=f"{total_working_years} Years"
    )

st.markdown("---")

# =========================================================
# PREDICTION BUTTON
# =========================================================

if st.button("🔍 Predict Attrition Risk"):

    try:

        prediction = model.predict(input_data)[0]

        probability = model.predict_proba(input_data)[0][1] * 100

        # =================================================
        # RISK LEVEL
        # =================================================

        if probability >= 70:
            risk = "🔴 HIGH RISK"
            recommendation = """
            - Immediate HR intervention required
            - Consider salary revision
            - Improve work-life balance
            - Conduct employee counseling
            """

        elif probability >= 40:
            risk = "🟠 MEDIUM RISK"
            recommendation = """
            - Monitor employee satisfaction
            - Improve engagement activities
            - Review workload management
            """

        else:
            risk = "🟢 LOW RISK"
            recommendation = """
            - Employee is stable
            - Continue engagement programs
            - Maintain positive work culture
            """

        # =================================================
        # RESULTS SECTION
        # =================================================

        st.success("Prediction Completed Successfully")

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("## 📈 Prediction Probability")

            st.metric(
                label="Attrition Probability",
                value=f"{probability:.2f}%"
            )

            st.progress(int(probability))

        with col2:

            st.markdown("## 🚨 Risk Category")

            st.info(risk)

            if prediction == 1:
                st.error("Employee likely to leave the organization.")
            else:
                st.success("Employee likely to stay.")

        st.markdown("---")

        # =================================================
        # HR RECOMMENDATIONS
        # =================================================

        st.markdown("## 💡 HR Recommendations")

        st.markdown(recommendation)

        # =================================================
        # EMPLOYEE SUMMARY
        # =================================================

        st.markdown("## 👨‍💼 Employee Summary")

        summary_df = pd.DataFrame({

            "Feature": [
                "Age",
                "Monthly Income",
                "Job Satisfaction",
                "Distance From Home",
                "Years At Company",
                "OverTime"
            ],

            "Value": [
                age,
                monthly_income,
                job_satisfaction,
                distance_from_home,
                years_at_company,
                "Yes" if overtime == 1 else "No"
            ]
        })

        st.dataframe(
            summary_df,
            use_container_width=True
        )

    except Exception as e:

        st.error(f"Prediction Error: {e}")

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown("""
<center>

### 📊 AI Employee Attrition Prediction System

Built using:
Python • Streamlit • Scikit-Learn • Random Forest

</center>
""", unsafe_allow_html=True)

