import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("72-hour Job Overflow Simulation")

# --- Input Section ---
st.sidebar.header("Input Settings")

weeks = st.sidebar.number_input("Number of weeks", min_value=1, max_value=10, value=5)

st.sidebar.subheader("Daily Capacity (Mon–Sun)")
capacity_mon = st.sidebar.number_input("Monday", value=35)
capacity_tue = st.sidebar.number_input("Tuesday", value=35)
capacity_wed = st.sidebar.number_input("Wednesday", value=35)
capacity_thu = st.sidebar.number_input("Thursday", value=10)
capacity_fri = st.sidebar.number_input("Friday", value=10)
capacity_sat = st.sidebar.number_input("Saturday", value=0)
capacity_sun = st.sidebar.number_input("Sunday", value=0)

capacity_pattern = np.array([
    capacity_mon, capacity_tue, capacity_wed,
    capacity_thu, capacity_fri, capacity_sat, capacity_sun
])
daily_capacity = np.tile(capacity_pattern, weeks)

st.sidebar.subheader("Job Inflow")
job_days = st.sidebar.multiselect(
    "Select weekdays for job inflow",
    ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    default=["Mon", "Fri"]
)
job_amount = st.sidebar.number_input("Jobs per selected day", value=100)

# Map weekday to index
weekday_map = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6}

# --- Simulation ---
days = weeks * 7
daily_inflow = np.zeros(days)
for i in range(weeks):
    for d in job_days:
        daily_inflow[i * 7 + weekday_map[d]] = job_amount

backlog_start = np.zeros(days)
backlog_end = np.zeros(days)
safe_limit = np.zeros(days)

remaining = 0

for i in range(days):
    backlog_start[i] = remaining + daily_inflow[i]
    processed = min(backlog_start[i], daily_capacity[i])
    backlog_end[i] = backlog_start[i] - processed
    remaining = backlog_end[i]
    safe_limit[i] = np.sum(daily_capacity[i:i + 3])

# --- Plot ---
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(backlog_start, marker="o", label="Backlog at Start of Day", color="blue")
ax.plot(safe_limit, "--", color="red", label="72-hour Capacity Limit")

# Highlight overflow points
for i in range(days):
    if backlog_start[i] > safe_limit[i]:
        ax.plot(i, backlog_start[i], "o", color="red")

ax.set_title("72-hour Completion Check")
ax.set_xlabel("Day")
ax.set_ylabel("Jobs Remaining")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# --- Summary ---
overflow_days = np.sum(backlog_start > safe_limit)
if overflow_days == 0:
    st.success("✅ No overflow detected within 72-hour limit.")
else:
    st.error(f"⚠️ Overflow detected on {overflow_days} day(s).")
