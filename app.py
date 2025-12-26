
import streamlit as st
import numpy as np
import pandas as pd

# ---------- Authentication ----------
def login():
    st.title("🔐 Secure CPS Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state["logged_in"] = True
        else:
            st.error("Invalid username or password")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
    st.stop()

# ---------- Dashboard ----------
st.title("🚰 Water Tank CPS – Security Supervisor")

steps = st.sidebar.slider("Simulation Steps", 50, 300, 200)
attack_step = st.sidebar.slider("Attack Start Step", 10, steps-10, 120)
attack_mag = st.sidebar.slider("Attack Magnitude", 1.0, 10.0, 5.0)

water = 50
safe_max = 100
alert_log = []
levels = []

def classify_alert(residual):
    if abs(residual) < 2:
        return "LOW"
    elif abs(residual) < 5:
        return "MEDIUM"
    else:
        return "HIGH"

for t in range(steps):
    inflow = 2
    measured = water + np.random.normal(0,0.5)

    if t > attack_step:
        measured += attack_mag

    residual = measured - water
    severity = classify_alert(residual)

    if severity == "HIGH":
        inflow = 0
        alert_log.append({"Time": t, "Severity": severity, "Action": "Mitigation Applied"})
    elif severity == "MEDIUM":
        alert_log.append({"Time": t, "Severity": severity, "Action": "Warning"})

    water += inflow
    water = min(water, safe_max)
    levels.append(water)

st.subheader("Water Level Over Time")
st.line_chart(levels)

st.subheader("🚨 Alert Log")
if alert_log:
    st.dataframe(pd.DataFrame(alert_log))
else:
    st.success("No attacks detected")
