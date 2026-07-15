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
# Page Configuration
# -----------------------------------
st.set_page_config(
    page_title="Venue Analysis",
    page_icon="🏟",
    layout="wide"
)

st.title("🏟 Venue Analysis")

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
# Venue Selection
# -----------------------------------
venues = sorted(matches["venue"].dropna().unique())

selected_venue = st.selectbox(
    "Select Venue",
    venues
)

# -----------------------------------
# Venue Matches
# -----------------------------------
venue_matches = matches[matches["venue"] == selected_venue]

match_ids = venue_matches["id"]

venue_deliveries = deliveries[
    deliveries["match_id"].isin(match_ids)
]

# -----------------------------------
# KPI Calculations
# -----------------------------------
matches_played = len(venue_matches)

teams = len(
    pd.concat(
        [
            venue_matches["team1"],
            venue_matches["team2"]
        ]
    ).unique()
)

avg_score = (
    venue_deliveries
    .groupby(["match_id", "inning"])["total_runs"]
    .sum()
    .mean()
)

highest_score = (
    venue_deliveries
    .groupby(["match_id", "inning"])["total_runs"]
    .sum()
    .max()
)

# -----------------------------------
# KPI Cards
# -----------------------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("🏏 Matches", matches_played)

c2.metric("👥 Teams", teams)

c3.metric("📊 Avg Innings Score", round(avg_score,1))

c4.metric("🔥 Highest Score", int(highest_score))

st.divider()

# ==========================================
# Tabs
# ==========================================

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

tab1, tab2, tab3 = st.tabs(
    [
        "📊 Overview",
        "🏏 Team Performance",
        "📅 Matches"
    ]
)

# ==========================================
# OVERVIEW
# ==========================================

with tab1:

    st.subheader("Matches Played Per Season")

    season_matches = (
        venue_matches
        .groupby("season")
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
    
    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Toss Winners")

    toss = (
        venue_matches["toss_winner"]
        .value_counts()
        .reset_index()
    )

    toss.columns = ["Team", "Toss Wins"]

    fig2 = px.pie(
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
        fig2,
        use_container_width=True
    )

# ==========================================
# TEAM PERFORMANCE
# ==========================================

with tab2:

    st.subheader("Matches Won by Teams")

    wins = (
        venue_matches["winner"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    wins.columns = ["Team", "Wins"]

    fig3 = px.bar(
        wins,
        x="Team",
        y="Wins",
        color="Wins"
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
        wins,
        use_container_width=True
    )

# ==========================================
# MATCHES
# ==========================================

with tab3:

    st.subheader("Recent Matches")

    recent = venue_matches.sort_values(
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
                "toss_winner",
                "venue"
            ]
        ].head(20),
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