import streamlit as st
from helpers import draw_stacked_bar

def render_watched(df):
    local_df = df.copy()
    # tab title
    st.markdown("<h1 style='text-align: center;'>Watched</h1>", unsafe_allow_html=True)

    # get the longest and shortest works by episodes
    filter_episodes = local_df.loc[:, ["title", "english_title", "episodes"]]

    filter_episodes = filter_episodes.dropna(subset="episodes")
    filter_episodes = filter_episodes.sort_values(by="episodes")

    shortest = filter_episodes.iloc[0:5]
    longest = filter_episodes.iloc[:-6:-1]

    # get genres and tags
    local_df["genres"] = local_df["genres"].str.split(";")
    local_df["tags"] = local_df["tags"].str.split(";")

    genres = local_df.explode("genres")["genres"].value_counts().sort_values(ascending=False)
    tags = local_df.explode("tags")["tags"].value_counts().sort_values(ascending=False)

    # get source distribution
    source = local_df.groupby("source")["source"].value_counts()
    source = source / len(local_df) * 100
    source = round(source,2)

    source_local_df = source.reset_index()
    source_local_df.columns = ["source", "share"]
    source_local_df = source_local_df.sort_values(by="share", ascending=False)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Shortest Anime")
        st.dataframe(shortest, hide_index=True, width="stretch")

    with col2: 
        st.markdown("### Longest Anime")
        st.dataframe(longest, hide_index=True, width="stretch")

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### Genres")
        st.dataframe(genres, height=210, width="stretch")

    with col4:
        st.markdown("### Tags")
        st.dataframe(tags, height=210, width="stretch")

    st.markdown("#### Source Share")
    draw_stacked_bar(source_local_df, "source", "share")
