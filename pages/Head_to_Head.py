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
    page_title="Head to Head Analysis",
    page_icon="⚔️",
    layout="wide"
)

st.title("⚔️ Head-to-Head Analysis")

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

col1, col2 = st.columns(2)

with col1:
    team1 = st.selectbox("Select Team 1", teams)

with col2:
    team2 = st.selectbox(
        "Select Team 2",
        [team for team in teams if team != team1]
    )

# -----------------------------------
# Filter Matches
# -----------------------------------
h2h = matches[
    (
        (matches["team1"] == team1) &
        (matches["team2"] == team2)
    )
    |
    (
        (matches["team1"] == team2) &
        (matches["team2"] == team1)
    )
]

if h2h.empty:
    st.warning("No matches found between these two teams.")
    st.stop()

# -----------------------------------
# KPI Cards
# -----------------------------------
total_matches = len(h2h)

team1_wins = len(h2h[h2h["winner"] == team1])

team2_wins = len(h2h[h2h["winner"] == team2])

no_result = total_matches - team1_wins - team2_wins

c1, c2, c3, c4 = st.columns(4)

c1.metric("🏏 Matches", total_matches)

c2.metric(team1, team1_wins)

c3.metric(team2, team2_wins)

c4.metric("No Result", no_result)

st.divider()

# =========================================
# Tabs
# =========================================

tab1, tab2, tab3 = st.tabs(
    [
        "📊 Overview",
        "📈 Statistics",
        "📅 Match History"
    ]
)

# =========================================
# OVERVIEW
# =========================================

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

with tab1:

    st.subheader("Head-to-Head Wins")

    wins = pd.DataFrame({
        "Team":[team1, team2],
        "Wins":[team1_wins, team2_wins]
    })

    fig = px.bar(
        wins,
        x="Team",
        y="Wins",
        color="Wins",
        text="Wins"
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

    st.subheader("Win Percentage")

    win_df = pd.DataFrame({
        "Team":[team1, team2],
        "Win %":[
            round((team1_wins/total_matches)*100,2),
            round((team2_wins/total_matches)*100,2)
        ]
    })

    fig2 = px.pie(
        win_df,
        names="Team",
        values="Win %"
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

# =========================================
# STATISTICS
# =========================================

with tab2:

    st.subheader("Toss Winners")

    toss = (
        h2h["toss_winner"]
        .value_counts()
        .reset_index()
    )

    toss.columns = ["Team","Toss Wins"]

    fig3 = px.bar(
        toss,
        x="Team",
        y="Toss Wins",
        color="Toss Wins"
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

    st.subheader("Match Results")

    st.dataframe(
        h2h[
            [
                "season",
                "winner",
                "player_of_match",
                "venue"
            ]
        ],
        use_container_width=True
    )

# =========================================
# MATCH HISTORY
# =========================================

with tab3:

    st.subheader("Recent Matches")

    recent = h2h.sort_values(
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
                "player_of_match",
                "venue"
            ]
        ],
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

