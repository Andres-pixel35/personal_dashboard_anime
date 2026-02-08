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
df["genres"] = df["genres"].str.split(";")
df["tags"] = df["tags"].str.split(";")

st.set_page_config(layout="wide")

with st.sidebar:
    st.header("Filters")

    choice_year = st.multiselect("Filter year:", sorted(df["start_date"].dt.year.unique()))
    choice_type = st.multiselect("Filter type:", df["type"].unique())
    choice_genre = st.multiselect("Filter genre", sorted(df.explode("genres")["genres"].unique()))
    choice_tag = st.multiselect("Filter tag", sorted(df.explode("tags")["tags"].unique()))

    st.info("You may choose more than one option")

# apply filters, provided they were chose 
if choice_type:
    df = df[df["type"].isin(choice_type)]

# 3. Apply Year Filter
if choice_year:
    df = df[df["start_date"].dt.year.isin(choice_year)]

# 4. Apply Genre Filter (Handles lists within cells)
if choice_genre:
    df = df[df["genres"].apply(lambda x: any(g in x for g in choice_genre))]

# 5. Apply Tag Filter (Handles lists within cells)
if choice_tag:
    df = df[df["tags"].apply(lambda x: any(t in x for t in choice_tag))]


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




