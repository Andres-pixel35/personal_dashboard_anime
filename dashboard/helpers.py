import streamlit as st
import altair as alt

def custom_metric(label, value, subtext):
    """
    Renders a custom metric with a caption/subtext beneath the value.
    """
    st.markdown(
        f"""
        <div style="text-align: center; padding: 10px;">
            <p style="font-size: 14px; margin-bottom: 4px; color: #808495; font-weight: 400;">{label}</p>
            <p style="font-size: 44px; font-weight: 400; margin: 0px; color: white; line-height: 1;">{value}</p>
            <p style="font-size: 14px; margin-top: 8px; color: #808495; font-weight: 400;">{subtext}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def draw_stacked_bar(df, category_col, value_col):
    category_order = df[category_col].tolist()

    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X(f"sum({value_col}):Q", stack="normalize", axis=None),
        color=alt.Color(
            f"{category_col}:N", 
            sort=category_order, #  Legend order
            scale=alt.Scale(scheme="tableau20"),
            legend=alt.Legend(orient="bottom", title=None)
        ),
        
        order=alt.Order(
            f"{value_col}:Q",
            sort="descending" # Ensures the largest value is the first stack (left side)
        ),
        tooltip=[f"{category_col}:N", f"{value_col}:Q"]
    ).properties(
        height=100
    ).configure_view(
        strokeOpacity=0
    )
    
    st.altair_chart(chart, width="stretch")
