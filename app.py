import streamlit as st
import pandas as pd
import numpy as np

# Dummy data setup
managers = ['Alice', 'Bob']
employees = {
    'Alice': ['John', 'Maria'],
    'Bob': ['Carlos', 'Ana']
}

kpis = ['Sales Conversion', 'CSAT', 'Attendance']
default_weights = {'Sales Conversion': 0.5, 'CSAT': 0.3, 'Attendance': 0.2}
threshold = 70
weeks = [f"Week {i+1}" for i in range(8)]

# Simulate KPI results per employee per week
def generate_dummy_scores():
    data = []
    for manager, team in employees.items():
        for emp in team:
            for week in weeks:
                kpi_scores = {kpi: np.random.randint(50, 100) for kpi in kpis}
                row = {
                    'Manager': manager,
                    'Employee': emp,
                    'Week': week,
                    **kpi_scores
                }
                data.append(row)
    return pd.DataFrame(data)

# Score calculation function
def calculate_score(row, weights):
    return sum([row[kpi] * weights[kpi] for kpi in kpis])

# Classification logic
def classify_employee(weekly_scores):
    below = (weekly_scores['Score'] < threshold).sum()
    if below >= 5:
        return "Recurring Deviation"
    elif below >= 1:
        return "Occasional Deviation"
    else:
        return "On Track"

# Streamlit UI
st.title("Performance Indicator Management Dashboard")

selected_manager = st.selectbox("Select Manager", managers)

# Load and filter data
data = generate_dummy_scores()
data = data[data['Manager'] == selected_manager]

# KPI weight configuration
st.sidebar.header("KPI Weights")
weights = {}
for kpi in kpis:
    weights[kpi] = st.sidebar.slider(f"{kpi} Weight", 0.0, 1.0, default_weights[kpi], 0.05)

# Normalize weights
total_weight = sum(weights.values())
if total_weight != 1.0:
    st.sidebar.warning("Weights do not sum to 1. Normalizing...")
    weights = {k: v / total_weight for k, v in weights.items()}

# Apply score calculation
data['Score'] = data.apply(lambda row: calculate_score(row, weights), axis=1)

# Weekly status flag
data['Status'] = data['Score'].apply(lambda x: 'Delivered' if x >= threshold else 'Not Delivered')

# Employee-level summary
employee_summary = data.groupby('Employee').apply(lambda df: pd.Series({
    'Weeks Below Target': (df['Score'] < threshold).sum(),
    'Classification': classify_employee(df)
})).reset_index()

st.subheader("Weekly Performance")
st.dataframe(data)

st.subheader("Employee Summary")
st.dataframe(employee_summary)

# Placeholder for manager actions (MVP)
st.subheader("Manager Actions")
selected_employee = st.selectbox("Select Employee", employee_summary['Employee'])
action_taken = st.text_area("Actions Taken / Planned")
if st.button("Submit Action"):
    st.success(f"Action for {selected_employee} submitted!")