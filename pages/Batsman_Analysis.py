import streamlit as st
import pandas as pd
import plotly.express as px

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

st.sidebar.success("Made by Ayush C using Streamlit")

# -----------------------------------
# Page Config
# -----------------------------------
st.set_page_config(
    page_title="Batsman Analysis",
    page_icon="🏏",
    layout="wide"
)

st.title("🏏 Batsman Analysis")

# -----------------------------------
# Load Data
# -----------------------------------
@st.cache_data
def load_data():
    matches = pd.read_csv("data/matches.csv")
    deliveries = pd.read_csv("data/deliveries.csv")
    return matches, deliveries

matches, deliveries = load_data()

# -----------------------------------
# Merge season into deliveries
# -----------------------------------
player_data = deliveries.merge(
    matches[["id", "season"]],
    left_on="match_id",
    right_on="id"
)

# -----------------------------------
# Player Dropdown
# -----------------------------------
players = sorted(player_data["batter"].dropna().unique())

selected_player = st.selectbox(
    "Select Player",
    players
)

player = player_data[player_data["batter"] == selected_player]

# -----------------------------------
# KPIs
# -----------------------------------
runs = player["batsman_runs"].sum()

balls = len(player)

strike_rate = round((runs / balls) * 100, 2) if balls > 0 else 0

fours = len(player[player["batsman_runs"] == 4])

sixes = len(player[player["batsman_runs"] == 6])

col1, col2, col3, col4 = st.columns(4)

col1.metric("🏏 Runs", runs)
col2.metric("⚾ Balls", balls)
col3.metric("⚡ Strike Rate", strike_rate)
col4.metric("💥 4s / 6s", f"{fours} / {sixes}")

st.divider()

# -----------------------------------
# Runs by Season
# -----------------------------------

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

season_runs = (
    player.groupby("season")["batsman_runs"]
    .sum()
    .reset_index()
)

fig = px.line(
    season_runs,
    x="season",
    y="batsman_runs",
    markers=True,
    title="Runs by Season"
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font=dict(size=15),
    title_x=0.5
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------
# Dismissal Types
# -----------------------------------
dismissals = deliveries[
    deliveries["player_dismissed"] == selected_player
]

if not dismissals.empty:

    dismissal_chart = (
        dismissals["dismissal_kind"]
        .value_counts()
        .reset_index()
    )

    dismissal_chart.columns = [
        "Dismissal",
        "Count"
    ]

    fig2 = px.pie(
        dismissal_chart,
        names="Dismissal",
        values="Count",
        title="Dismissal Types"
    )
    
    fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font=dict(size=15),
    title_x=0.5
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# -----------------------------------
# Runs Against Teams
# -----------------------------------
team_runs = (
    player.groupby("bowling_team")["batsman_runs"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig3 = px.bar(
    team_runs,
    x="bowling_team",
    y="batsman_runs",
    title="Runs Against Teams"
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font=dict(size=15),
    title_x=0.5
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# -----------------------------------
# Recent Deliveries
# -----------------------------------
st.subheader("Recent Deliveries")

st.dataframe(
    player[
        [
            "season",
            "batting_team",
            "bowling_team",
            "bowler",
            "batsman_runs"
        ]
    ].tail(20),
    use_container_width=True
)

st.markdown("---")

st.markdown(
"""
<center>

Built by Ayush C using

Python • Pandas • Plotly • Streamlit • Scikit-Learn

</center>
""",
unsafe_allow_html=True
)