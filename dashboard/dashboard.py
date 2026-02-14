import pandas as pd
import streamlit as st
from tabs import time, score, watched, summarize, database
import sys
import os

# Add the parent directory (root) to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import path_final_csv, user_name

df = pd.read_csv(path_final_csv)

df_fil = df.copy()

df_fil["start_date"] = pd.to_datetime(df_fil["start_date"])
df_fil["genres"] = df_fil["genres"].str.split(";")
df_fil["tags"] = df_fil["tags"].str.split(";")

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

with st.sidebar:
    st.header("Filters")

    choice_year = st.multiselect("Filter year:", sorted(df_fil["start_date"].dt.year.unique(), reverse=True))
    choice_type = st.multiselect("Filter type:", df_fil["type"].unique())
    choice_genre = st.multiselect("Filter genre", sorted(df_fil.explode("genres")["genres"].unique()))
    choice_tag = st.multiselect("Filter tag", sorted(df_fil.explode("tags")["tags"].unique()))
    choice_source = st.multiselect("Filter source", df_fil["source"].unique())
    choice_season = st.multiselect("Filter season", df_fil["season"].unique())
    choice_country = st.multiselect("Filter country", df_fil["country_of_origin"].unique())

    st.info("You may choose more than one option")

# apply filters, provided they were chose 
if choice_type:
    df_fil = df_fil[df_fil["type"].isin(choice_type)]

if choice_year:
    df_fil = df_fil[df_fil["start_date"].dt.year.isin(choice_year)]

if choice_genre:
    df_fil = df_fil[df_fil["genres"].apply(lambda x: any(g in x for g in choice_genre))]

if choice_tag:
    df_fil = df_fil[df_fil["tags"].apply(lambda x: any(t in x for t in choice_tag))]

if choice_source:
    df_fil = df_fil[df_fil["source"].isin(choice_source)]

if choice_season:
    df_fil = df_fil[df_fil["season"].isin(choice_season)]

if choice_country:
    df_fil = df_fil[df_fil["country_of_origin"].isin(choice_country)]

if df_fil.empty:
    st.warning("No data found for the selected filter(s). Try picking a different filter!")
else:

    st.title(f"{user_name}'s Anime Dashboard")

    #  tabs names
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Summarize", "Watched", "Time", "Score", "Database"])

    # Content for Tab 1
    with tab1:
        summarize.render_summarize(df_fil)

    # Content for Tab 2
    with tab2:
        watched.render_watched(df_fil)

    # Content for Tab 3
    with tab3:
        time.render_time(df_fil)

    # Content for Tab 4
    with tab4:
        score.render_score(df_fil)

    # Content for Tab 5
    with tab5:
        database.render_database(df_fil)





