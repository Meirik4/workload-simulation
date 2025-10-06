import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("📊 72-Hour Workload Simulation")

st.write("Set daily capacities and order inflows for each weekday, and observe the backlog trends.")

# --- Input Section ---
st.sidebar.header("🗓 Settings per Weekday")

weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# Daily processing capacity
st.sidebar.subheader("Processing Capacity (per day)")
capacity_pattern = []
for day in weekdays:
    val = st.sidebar.number_input(
        f"{day}", min_value=0, max_value=200, 
        value=35 if day in ["Mon", "Tue", "Wed"] else (10 if day in ["Thu", "Fri"] else 0)
    )
    capacity_pattern.append(val)

# Daily order inflow
st.sidebar.subheader("Order Inflow (per day)")
inflow_pattern = []
for day in weekdays:
    val = st.sidebar.number_input(
        f"{day} Order Inflow", min_value=0, max_value=200, 
        value=100 if day == "Mon" else (10 if day == "Fri" else 0)
    )
    inflow_pattern.append(val)

weeks = st.sidebar.slider("Number of Weeks to Simulate", 1, 8, 5)
days = weeks * 7

# --- Data Generation ---
daily_capacity = np.tile(capacity_pattern, weeks)
daily_inflow = np.tile(inflow_pattern, weeks)

# --- Backlog Calculation ---
backlog_start = np.zeros(days)
backlog_end = np.zeros(days)
remaining = 0

for i in range(days):
    backlog_start[i] = remaining + daily_inflow[i]
    processed = min(backlog_start[i], daily_capacity[i])
    backlog_end[i] = backlog_start[i] - processed
    remaining = backlog_end[i]

# --- 72-Hour Capacity ---
safe_limit = np.zeros(days)
for i in range(days):
    safe_limit[i] = np.sum(daily_capacity[i:i+3])

# --- Plotting ---
plt.figure(figsize=(10, 5))
plt.plot(backlog_start, marker="o", label="Backlog (Start of Day)", color="blue")
plt.plot(safe_limit, "--", color="red", label="72-Hour Processing Capacity")

# Highlight exceeding points
for i in range(days):
    if backlog_start[i] > safe_limit[i]:
        plt.scatter(i, backlog_start[i], color="red", s=50, zorder=3)

plt.title("72-Hour Workload Simulation")
plt.xlabel("Days (0 = First Monday)")
plt.ylabel("Work Amount")
plt.legend()
plt.grid(True)
st.pyplot(plt)

# --- Result Message ---
overdue_days = np.sum(backlog_start > safe_limit)
if overdue_days == 0:
    st.success("🌟 All work can be processed within 72 hours!")
else:
    st.error(f"⚠️ Work exceeding 72 hours occurs on {overdue_days} day(s).")
