import streamlit as st
import pandas as pd
import plotly.express as px

from utils.components import hero
from utils.components import feature_card
from utils.components import insight_card
from utils.components import section

# -------------------------
# Page Config
# -------------------------

st.set_page_config(
    page_title="IPL Analytics Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

# -------------------------
# Load Data
# -------------------------
@st.cache_data
def load_data():
    matches = pd.read_csv("data/matches.csv")
    deliveries = pd.read_csv("data/deliveries.csv")
    return matches, deliveries

matches, deliveries = load_data()

# -------------------------
# Dashboard Title
# -------------------------
# -------------------------
# Hero Section
# -------------------------

st.markdown("""
<div class="hero">

<h1>🏏 IPL Analytics Dashboard</h1>

<p>
End-to-End Data Analytics & Machine Learning Project
</p>

</div>
""",unsafe_allow_html=True)

# ==========================
# KPI Cards
# ==========================

total_matches = matches.shape[0]

total_teams = len(
    pd.concat(
        [matches["team1"], matches["team2"]]
    ).unique()
)

total_players = deliveries["batter"].nunique()

total_seasons = matches["season"].nunique()

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    label="🏏 Total Matches",
    value=total_matches
)

c2.metric(
    label="👥 Teams",
    value=total_teams
)

c3.metric(
    label="👤 Players",
    value=total_players
)

c4.metric(
    label="📅 Seasons",
    value=total_seasons
)

st.markdown("---")

# ==========================
# Two Column Layout
# ==========================

def update_chart(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Poppins",
            size=15,
            color="white"
        ),
        title_x=0.5,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    return fig
left, right = st.columns([2,1])

# --------------------------
# Left
# --------------------------

with left:

    st.subheader("Matches Played Per Season")

    season_matches = (
        matches.groupby("season")
        .size()
        .reset_index(name="Matches")
    )

    fig = px.line(
        season_matches,
        x="season",
        y="Matches",
        markers=True
    )
    
    fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font=dict(size=15),
    title_x=0.5
    )

    fig.update_layout(height=420)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# --------------------------
# Right
# --------------------------

with right:

    st.subheader("Top 10 Teams")

    wins = (
        matches["winner"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    wins.columns = ["Team","Wins"]

    fig2 = px.bar(
        wins,
        x="Wins",
        y="Team",
        orientation="h"
    )

    fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font=dict(size=15),
    title_x=0.5
    )
    
    fig2.update_layout(height=420)

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

st.markdown("---")

# ==========================
# Overview
# ==========================

st.subheader("Project Overview")

st.info("""
This dashboard provides:

✔ Team Analysis

✔ Player Analysis

✔ Venue Analysis

✔ Head-to-Head Comparison

✔ Bowler Analysis

✔ Win Prediction

✔ Interactive Visualizations
""")

st.markdown("---")

section("🔥 Dashboard Highlights")

c1,c2,c3,c4 = st.columns(4)

with c1:
    insight_card(
        "🏆",
        "Most Successful Team",
        matches["winner"].value_counts().idxmax()
    )

with c2:
    insight_card(
        "👑",
        "Top Run Scorer",
        deliveries.groupby("batter")["batsman_runs"].sum().idxmax()
    )

with c3:
    insight_card(
        "🎯",
        "Top Wicket Taker",
        deliveries["bowler"].value_counts().idxmax()
    )

with c4:
    insight_card(
        "📅",
        "Total Seasons",
        matches["season"].nunique()
    )

st.markdown("---")

st.markdown(
"""
<center>

Built by <b>Ayush C</b> using

Python • Pandas • Plotly • Streamlit • Scikit-Learn

</center>
""",
unsafe_allow_html=True
)