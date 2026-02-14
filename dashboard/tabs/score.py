import streamlit as st

def render_score(df):
    local_df = df.copy()

    st.markdown("<h1 style='text-align: center;'>Score</h1>", unsafe_allow_html=True)

    # get worst and best scored works
    score = local_df.loc[:, ["title", "english_title", "score"]]
    score = score.sort_values(by="score")

    worst = score.iloc[0:5]
    best = score[:-6:-1]

    # get score distribution
    score_distribution = local_df.groupby("score")["score"].value_counts().sort_index()

    # change columns name
    columns = {
        "title": "Title",
        "english_title": "English Title",
        "score": "Score"
    }

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Five Worst Ranked Anime")
        st.dataframe(worst, hide_index=True, width="stretch", column_config=columns)

    with col2:
        st.markdown("### Five Best Ranked Anime")
        st.dataframe(best, hide_index=True, width="stretch", column_config=columns)

    st.markdown("#### Score Distribution")
    st.bar_chart(score_distribution, x_label="Score", y_label="Frequency")


