import streamlit as st

def render_database(df):
    local_df = df.copy()

    local_df["start_date"] = local_df["start_date"].dt.date

    local_df = local_df.drop(columns=["complete_duration"])

    st.dataframe(local_df, hide_index=True, height=559,
                 column_config={
                 "title": "Title",
                 "english_title": "English Title",
                 "type": "Type",
                 "episodes": "Episodes",
                 "duration": "Duration",
                 "source": "Source",
                 "season": "Season",
                 "genres": "Genres",
                 "tags": "Tags",
                 "score": "Score",
                 "start_date": "Start Date",
                 "country_of_origin": "Country of Origin"
                 })

    st.info("You can sort each column either to ascending or decesding by cliking it")

