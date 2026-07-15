import streamlit as st

# -----------------------
# Load CSS
# -----------------------
def load_css():
    with open("assets/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

# -----------------------
# Sidebar
# -----------------------
def sidebar():

    st.sidebar.image(
        "assets/ipl_logo.png",
        width=170
    )

    st.sidebar.title("🏏 IPL Analytics")

    st.sidebar.markdown("---")

    st.sidebar.success("AI & Data Science Project")

# -----------------------
# Hero
# -----------------------
def hero(title, subtitle):

    st.markdown(f"""
    <div style="
    background:linear-gradient(135deg,#FF6B00,#F97316);
    padding:35px;
    border-radius:20px;
    box-shadow:0 12px 30px rgba(255,107,0,.30);
    ">

    <h1 style="color:white;text-align:center;">
    {title}
    </h1>

    <h4 style="color:white;text-align:center;">
    {subtitle}
    </h4>

    </div>

    """, unsafe_allow_html=True)

# -----------------------
# Plotly Theme
# -----------------------
def style_plot(fig):

    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="#111827",

        plot_bgcolor="#111827",

        font=dict(size=15),

        title_x=0.5,

        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        )
    )

    return fig

# -----------------------
# Footer
# -----------------------
def footer():

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