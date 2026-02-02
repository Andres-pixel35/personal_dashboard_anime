import pandas as pd
import streamlit as st

def render_time(df):
    local_df = df.copy()
    # tab's title
    st.markdown("<h1 style='text-align: center;'>Time</h1>", unsafe_allow_html=True)
    
    # get the amount of anime per each year
    local_df["start_date"] = pd.to_datetime(local_df["start_date"])
    years = local_df["start_date"].dt.year.value_counts().sort_index()

    # get older anime
    local_df["start_date"] = local_df["start_date"].dt.date
    old = local_df.loc[:, ["title", "english_title", "start_date"]]    
    old = old.sort_values(by="start_date")
    oldest = old.iloc[0:5]
    newest = old.iloc[:-6:-1]

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Newest Anime")
        st.dataframe(newest, hide_index=True, width="stretch")

    with col2:
        st.markdown("### Oldest Anime")
        st.dataframe(oldest, hide_index=True, width="stretch")
    
    st.markdown("#### Release Year Distribution")
    st.bar_chart(years, y_label="Frequency", x_label="Year")






