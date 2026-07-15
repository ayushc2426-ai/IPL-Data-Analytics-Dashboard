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

st.sidebar.success("Made with ❤️ using Streamlit")

# -----------------------------------
# Page Config
# -----------------------------------
st.set_page_config(
    page_title="Team Analysis",
    page_icon="🏏",
    layout="wide"
)

st.title("🏏 Team Analysis")

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
# Team Selection
# -----------------------------------
teams = sorted(pd.concat([matches["team1"], matches["team2"]]).dropna().unique())

selected_team = st.selectbox(
    "Select Team",
    teams
)

# -----------------------------------
# Team Matches
# -----------------------------------
team_matches = matches[
    (matches["team1"] == selected_team) |
    (matches["team2"] == selected_team)
]

# -----------------------------------
# KPI Calculations
# -----------------------------------
matches_played = len(team_matches)

matches_won = len(matches[matches["winner"] == selected_team])

win_percentage = round(
    (matches_won / matches_played) * 100,
    2
) if matches_played > 0 else 0

titles = matches[
    (matches["winner"] == selected_team) &
    (matches["match_type"] == "Final")
].shape[0] if "match_type" in matches.columns else 0

# -----------------------------------
# KPI Cards
# -----------------------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("🏏 Matches", matches_played)
c2.metric("🏆 Wins", matches_won)
c3.metric("📈 Win %", f"{win_percentage}%")
c4.metric("👑 Titles", titles)

st.divider()

# ===========================================
# TABS
# ===========================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📊 Overview",
        "🏏 Batting",
        "🎯 Bowling",
        "📅 Matches"
    ]
)

# ===========================================
# OVERVIEW
# ===========================================

with tab1:

    st.subheader("Wins by Season")

    season_wins = (
        matches[matches["winner"] == selected_team]
        .groupby("season")
        .size()
        .reset_index(name="Wins")
    )

    fig = px.line(
        season_wins,
        x="season",
        y="Wins",
        markers=True
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

    st.subheader("Venue Distribution")

    venue_chart = (
        team_matches["venue"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    venue_chart.columns = ["Venue", "Matches"]

    fig2 = px.bar(
        venue_chart,
        x="Venue",
        y="Matches"
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

# ===========================================
# BATTING
# ===========================================

with tab2:

    st.subheader("Top 10 Run Scorers")

    batting = deliveries[
        deliveries["batting_team"] == selected_team
    ]

    top_batters = (
        batting.groupby("batter")["batsman_runs"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig3 = px.bar(
        top_batters,
        x="batter",
        y="batsman_runs",
        color="batsman_runs"
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

    st.dataframe(
        top_batters,
        use_container_width=True
    )

# ===========================================
# BOWLING
# ===========================================

with tab3:

    st.subheader("Top 10 Wicket Takers")

    bowling = deliveries[
        deliveries["bowling_team"] == selected_team
    ]

    wickets = bowling[
        bowling["player_dismissed"].notna()
    ]

    top_bowlers = (
        wickets["bowler"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_bowlers.columns = [
        "Bowler",
        "Wickets"
    ]

    fig4 = px.bar(
        top_bowlers,
        x="Bowler",
        y="Wickets",
        color="Wickets"
    )
    
    fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font=dict(size=15),
    title_x=0.5
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

    st.dataframe(
        top_bowlers,
        use_container_width=True
    )

# ===========================================
# MATCHES
# ===========================================

with tab4:

    st.subheader("Recent Matches")

    recent = team_matches.sort_values(
        by="date",
        ascending=False
    )

    st.dataframe(
        recent[
            [
                "season",
                "date",
                "team1",
                "team2",
                "winner",
                "venue"
            ]
        ].head(10),
        use_container_width=True
    )

    st.subheader("Toss Winners")

    toss = (
        team_matches["toss_winner"]
        .value_counts()
        .reset_index()
    )

    toss.columns = [
        "Team",
        "Toss Wins"
    ]

    fig5 = px.pie(
        toss,
        names="Team",
        values="Toss Wins"
    )
    
    fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font=dict(size=15),
    title_x=0.5
    )
    
    st.plotly_chart(
        fig5,
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