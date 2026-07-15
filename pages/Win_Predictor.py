import streamlit as st
import pandas as pd
import joblib

def load_css():
    with open("assets/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/en/8/84/Indian_Premier_League_Official_Logo.svg",
    width=180
)

st.sidebar.title("🏏 IPL Dashboard")

st.sidebar.markdown("---")

st.sidebar.success("Made with ❤️ using Streamlit")

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="IPL Win Predictor",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 IPL Win Predictor")

# -----------------------------
# Load Model
# -----------------------------
model = joblib.load("models/pipe.pkl")

# -----------------------------
# Load Dataset
# -----------------------------
matches = pd.read_csv("data/matches.csv")

teams = sorted(pd.concat([matches["team1"], matches["team2"]]).dropna().unique())

cities = sorted(matches["city"].dropna().unique())

# -----------------------------
# Inputs
# -----------------------------

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox("Batting Team", teams)

with col2:
    bowling_team = st.selectbox(
        "Bowling Team",
        [team for team in teams if team != batting_team]
    )

city = st.selectbox("City", cities)

target = st.number_input(
    "Target",
    min_value=1,
    value=180
)

col3, col4, col5 = st.columns(3)

with col3:
    score = st.number_input(
        "Current Score",
        min_value=0,
        value=100
    )

with col4:
    overs = st.number_input(
        "Overs Completed",
        min_value=0.1,
        max_value=20.0,
        value=10.0,
        step=0.1
    )

with col5:
    wickets = st.number_input(
        "Wickets Lost",
        min_value=0,
        max_value=10,
        value=3
    )

# -----------------------------
# Prediction
# -----------------------------

if st.button("Predict Winning Probability"):

    balls_bowled = int(overs * 6)

    balls_left = 120 - balls_bowled

    runs_left = target - score

    wickets_left = 10 - wickets

    current_rr = score * 6 / balls_bowled if balls_bowled > 0 else 0

    required_rr = (
        runs_left * 6 / balls_left
        if balls_left > 0 else 0
    )

    pressure_index = required_rr - current_rr

    if overs <= 6:
        phase = "Powerplay"
    elif overs <= 15:
        phase = "Middle"
    else:
        phase = "Death"

    input_df = pd.DataFrame({
        "batting_team": [batting_team],
        "bowling_team": [bowling_team],
        "city": [city],
        "runs_left": [runs_left],
        "balls_left": [balls_left],
        "wickets_left": [wickets_left],
        "target_runs": [target],
        "current_rr": [current_rr],
        "required_rr": [required_rr],
        "pressure_index": [pressure_index],
        "phase": [phase]
    })

    probability = model.predict_proba(input_df)

    batting_win = probability[0][1] * 100
    bowling_win = probability[0][0] * 100

    st.divider()

    st.subheader("🏆 Winning Probability")

    c1, c2 = st.columns(2)

    c1.metric(
        batting_team,
        f"{batting_win:.2f}%"
    )

    c2.metric(
        bowling_team,
        f"{bowling_win:.2f}%"
    )

    st.progress(int(batting_win))
    
    st.markdown("---")

st.markdown(
"""
<center>

Built Ayush C using

Python • Pandas • Plotly • Streamlit • Scikit-Learn

</center>
""",
unsafe_allow_html=True
)