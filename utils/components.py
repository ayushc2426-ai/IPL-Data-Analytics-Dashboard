import streamlit as st


def hero(title, subtitle):

    st.markdown(f"""
    <div style="
    background:linear-gradient(135deg,#FF6B00,#F97316);
    padding:40px;
    border-radius:20px;
    box-shadow:0px 12px 25px rgba(0,0,0,.35);
    ">

    <h1 style="
    color:white;
    text-align:center;
    font-size:48px;
    margin-bottom:8px;
    ">

    {title}

    </h1>

    <h3 style="
    color:white;
    text-align:center;
    ">

    {subtitle}

    </h3>

    </div>

    """, unsafe_allow_html=True)



def section(title):

    st.markdown(f"""

    <h2 style="color:white;margin-top:15px;">

    {title}

    </h2>

    """, unsafe_allow_html=True)



def feature_card(icon, title, text):

    st.markdown(f"""

    <div style="
    background:#162032;
    padding:22px;
    border-radius:18px;
    border:1px solid #334155;
    height:180px;
    ">

    <h1>{icon}</h1>

    <h3 style="color:white">

    {title}

    </h3>

    <p style="color:#CBD5E1">

    {text}

    </p>

    </div>

    """, unsafe_allow_html=True)



def insight_card(icon, title, value):

    st.markdown(f"""

    <div style="
    background:#162032;
    padding:18px;
    border-radius:15px;
    border-left:6px solid #FF6B00;
    ">

    <h4>{icon} {title}</h4>

    <h2 style="color:white">

    {value}

    </h2>

    </div>

    """, unsafe_allow_html=True)