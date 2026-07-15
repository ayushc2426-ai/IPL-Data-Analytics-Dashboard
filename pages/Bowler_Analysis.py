import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------
# Load CSS
# -------------------------
def load_css():
    with open("assets/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="Bowler Analysis",
    page_icon="🎯",
    layout="wide"
)

# -------------------------
# Sidebar
# -------------------------
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
# Hero Section
# -------------------------
st.markdown("""
# 🎯 Bowler Analysis

### Explore Bowling Performance Across IPL Seasons

Analyze Wickets • Economy • Strike Rate • Dot Balls
""")

st.divider()

# -------------------------
# Bowler Selection
# -------------------------
bowlers = sorted(deliveries["bowler"].dropna().unique())

selected_bowler = st.selectbox(
    "Select Bowler",
    bowlers
)

bowler_df = deliveries[
    deliveries["bowler"] == selected_bowler
]

# -------------------------
# Bowling Statistics
# -------------------------

matches_played = bowler_df["match_id"].nunique()

balls = len(
    bowler_df[
        bowler_df["extras_type"] != "wides"
    ]
)

overs = round(balls / 6, 1)

runs = bowler_df["total_runs"].sum()

wickets = bowler_df[
    bowler_df["dismissal_kind"].notna()
]

wickets = wickets[
    ~wickets["dismissal_kind"].isin([
        "run out",
        "retired hurt",
        "obstructing the field"
    ])
]

wicket_count = wickets.shape[0]

economy = round(runs / overs, 2) if overs > 0 else 0

strike_rate = round(
    balls / wicket_count,
    2
) if wicket_count > 0 else 0

dot_balls = bowler_df[
    bowler_df["total_runs"] == 0
].shape[0]

dot_percentage = round(
    (dot_balls / balls) * 100,
    2
) if balls > 0 else 0

# -------------------------
# KPI Cards
# -------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "🏏 Matches",
    matches_played
)

c2.metric(
    "🎯 Wickets",
    wicket_count
)

c3.metric(
    "💰 Economy",
    economy
)

c4.metric(
    "⚡ Strike Rate",
    strike_rate
)

st.divider()

# -------------------------
# Tabs
# -------------------------

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
        "📈 Performance",
        "📋 Statistics"
    ]
)
with tab1:

    left, right = st.columns([1, 1])

    # ====================================
    # Wickets by Dismissal Type
    # ====================================

    with left:

        st.subheader("🎯 Wickets by Dismissal Type")

        dismissals = wickets["dismissal_kind"].value_counts().reset_index()
        dismissals.columns = ["Dismissal", "Count"]

        fig1 = px.bar(
            dismissals,
            x="Dismissal",
            y="Count",
            text="Count",
            color="Count",
            color_continuous_scale="Oranges"
        )

        fig1.update_layout(
            template="plotly_dark",
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            title_x=0.5,
            height=420,
            xaxis_title="",
            yaxis_title="Wickets"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    # ====================================
    # Dot Balls vs Scoring Balls
    # ====================================

    with right:

        st.subheader("🏏 Dot Ball Percentage")

        dot_df = pd.DataFrame({

            "Type": [
                "Dot Balls",
                "Scoring Balls"
            ],

            "Balls": [
                dot_balls,
                balls - dot_balls
            ]

        })

        fig2 = px.pie(
            dot_df,
            names="Type",
            values="Balls",
            hole=0.45
        )

        fig2.update_layout(
            template="plotly_dark",
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            height=420
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    st.markdown("---")

    # ====================================
    # Bowling Summary
    # ====================================

    st.subheader("📋 Bowling Summary")

    summary = pd.DataFrame({

        "Statistic": [

            "Matches Played",
            "Overs Bowled",
            "Runs Conceded",
            "Wickets",
            "Economy",
            "Strike Rate",
            "Dot Balls",
            "Dot Ball %"

        ],

        "Value": [

            matches_played,
            overs,
            runs,
            wicket_count,
            economy,
            strike_rate,
            dot_balls,
            f"{dot_percentage}%"

        ]

    })

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")

    # ====================================
    # Bowling Performance Rating
    # ====================================

    st.subheader("⭐ Bowling Performance")

    score = (
        wicket_count * 4
        + dot_percentage
        - economy * 3
    )

    score = max(0, min(score, 100))

    st.progress(score / 100)

    st.success(
        f"Performance Score : **{round(score,1)}/100**"
    )
    
    # ==========================================
# PERFORMANCE TAB
# ==========================================

with tab2:

    left, right = st.columns(2)

    # -----------------------------
    # Runs Conceded Per Over
    # -----------------------------
    with left:

        st.subheader("🏏 Runs Conceded Per Over")

        over_runs = (
            bowler_df
            .groupby("over")["total_runs"]
            .sum()
            .reset_index()
        )

        fig3 = px.line(
            over_runs,
            x="over",
            y="total_runs",
            markers=True
        )

        fig3.update_layout(
            template="plotly_dark",
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            title_x=0.5,
            height=420,
            xaxis_title="Over",
            yaxis_title="Runs"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

    # -----------------------------
    # Wickets by Over
    # -----------------------------
    with right:

        st.subheader("🎯 Wickets by Over")

        wicket_over = (
            wickets
            .groupby("over")
            .size()
            .reset_index(name="Wickets")
        )

        fig4 = px.bar(
            wicket_over,
            x="over",
            y="Wickets",
            text="Wickets",
            color="Wickets",
            color_continuous_scale="Oranges"
        )

        fig4.update_layout(
            template="plotly_dark",
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            title_x=0.5,
            height=420
        )

        st.plotly_chart(
            fig4,
            use_container_width=True
        )

    st.markdown("---")

    st.subheader("📈 Bowling Performance Summary")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "🏏 Balls Bowled",
        balls
    )

    c2.metric(
        "⚪ Dot Balls",
        dot_balls
    )

    c3.metric(
        "📊 Dot Ball %",
        f"{dot_percentage}%"
    )
    
    # ==========================================
# STATISTICS TAB
# ==========================================

with tab3:

    st.subheader("📋 Ball-by-Ball Statistics")

    stats = bowler_df[
        [
            "match_id",
            "inning",
            "over",
            "ball",
            "batting_team",
            "batter",
            "total_runs",
            "is_wicket"
        ]
    ].copy()

    stats.columns = [
        "Match ID",
        "Innings",
        "Over",
        "Ball",
        "Batting Team",
        "Batter",
        "Runs",
        "Wicket"
    ]

    st.dataframe(
        stats,
        use_container_width=True,
        height=500
    )

    st.markdown("---")

    st.subheader("📊 Overall Bowling Summary")

    summary = pd.DataFrame({

        "Statistic":[
            "Matches",
            "Overs",
            "Runs",
            "Wickets",
            "Economy",
            "Strike Rate",
            "Dot Ball %"
        ],

        "Value":[
            matches_played,
            overs,
            runs,
            wicket_count,
            economy,
            strike_rate,
            dot_percentage
        ]

    })

    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
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