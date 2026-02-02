import pandas as pd
import streamlit as st
from tabs import time, score, watched, summarize
import sys
import os

# Add the parent directory (root) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import path_final_csv, user_name

df = pd.read_csv(path_final_csv)

df["start_date"] = pd.to_datetime(df["start_date"])

st.set_page_config(layout="wide")

with st.sidebar:
    st.header("Filters")
    choice_year = st.multiselect("Filter year", sorted(df["start_date"].dt.year.unique()))
    type_choice = st.multiselect("Filter type:", df["type"].unique())

    st.info("You may choose more than one option")

# apply filters, provided they were chose 
if type_choice and choice_year:
    df = df[(df['type'].isin(type_choice)) & (df["start_date"].dt.year.isin(choice_year))]
elif type_choice:
    df = df[df["type"].isin(type_choice)]
elif choice_year:
    df = df[df["start_date"].dt.year.isin(choice_year)]

if df.empty:
    st.warning("No data found for the selected year(s) or/and type(s). Try picking a different filter!")
else:

    st.title(f"{user_name}'s Anime Dashboard")

    #  tabs names
    tab1, tab2, tab3, tab4 = st.tabs(["Summarize", "Watched", "Time", "Score"])

    # Content for Tab 1
    with tab1:
        summarize.render_summarize(df)

    # Content for Tab 2
    with tab2:
        watched.render_watched(df)

    # Content for Tab 3
    with tab3:
        time.render_time(df)

    # Content for Tab 4
    with tab4:
        score.render_score(df)




