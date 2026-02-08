import pandas as pd
import streamlit as st
from helpers import custom_metric

def render_summarize(df):
    local_df = df.copy()
    st.markdown("<h1 style='text-align: center;'>Thus Far, You've...</h1>", unsafe_allow_html=True)

    # get all the rows from the data frame (total works added)
    total_works = len(local_df)

    # get unique years
    local_df["start_date"] = pd.to_datetime(local_df["start_date"])
    unique_years = local_df["start_date"].dt.year.unique()
    amount_year = len(unique_years)

    # get mean score
    mean_score = int(round(local_df["score"].mean(), 0))

    # calculate day spent watching anime
    minutes = local_df["complete_duration"].sum()
    hours = round(minutes / 60, 0)
    days = int(round(hours / 24, 0))

    # calculate total episodes
    episodes = local_df["episodes"].sum()
    episodes = int(episodes)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        custom_metric("Watched", total_works, "Anime")

    with col2:
        custom_metric("Through", amount_year, "Different Years")

    with col3:
        custom_metric("With a", mean_score, "Score Mean")

    with col4:
        custom_metric("Spending", days, "Days")

    with col5:
        custom_metric("Watching", episodes, "Episodes")

    st.divider()

    st.markdown("<h1 style='text-align: center;'>Being your favourites...</h1>", unsafe_allow_html=True)

    genres = local_df.explode("genres")["genres"].value_counts().sort_values(ascending=False)
    tags = local_df.explode("tags")["tags"].value_counts().sort_values(ascending=False)

    # get favourite year 
    local_df["start_date"] = pd.to_datetime(local_df["start_date"]).dt.year
    years = local_df.groupby("start_date")["start_date"].value_counts().sort_values(ascending=False)

    col1, col2, col3 = st.columns(3)

    with col1:
        custom_metric("Genre", genres.index[0], f"{genres.iloc[0]} Apparitions")

    with col2:
        custom_metric("Tag", tags.index[0], f"{tags.iloc[0]} Apparitions")
    
    with col3:
        custom_metric("Year", years.index[0], f"{years.iloc[0]} Animes Watched")


