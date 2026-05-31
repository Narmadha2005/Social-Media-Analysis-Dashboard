import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------
# PAGE CONFIG
# ---------------------------

st.set_page_config(
    page_title="Social Media Analytics Dashboard",
    layout="wide"
)

# ---------------------------
# LOAD DATA
# ---------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("Data LIWC 01 02 23.csv")

    df["Engagement"] = (
        df["like_count"]
        + df["retweet_count"]
        + df["reply_count"]
        + df["quote_count"]
    )

    return df

df = load_data()

# ---------------------------
# TITLE
# ---------------------------

st.title("📊 Social Media Engagement Analytics Dashboard")

st.markdown("---")

# ---------------------------
# SIDEBAR FILTERS
# ---------------------------

st.sidebar.header("Filters")

state = st.sidebar.multiselect(
    "Select State",
    df["State"].unique(),
    default=df["State"].unique()
)

content_type = st.sidebar.multiselect(
    "Content Type",
    df["ContentType"].dropna().unique(),
    default=df["ContentType"].dropna().unique()
)

filtered_df = df[
    (df["State"].isin(state)) &
    (df["ContentType"].isin(content_type))
]

# ---------------------------
# KPI CARDS
# ---------------------------

total_posts = len(filtered_df)
total_likes = filtered_df["like_count"].sum()
total_retweets = filtered_df["retweet_count"].sum()
total_replies = filtered_df["reply_count"].sum()
total_engagement = filtered_df["Engagement"].sum()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Posts", f"{total_posts:,}")
col2.metric("Likes", f"{int(total_likes):,}")
col3.metric("Retweets", f"{int(total_retweets):,}")
col4.metric("Replies", f"{int(total_replies):,}")
col5.metric("Engagement", f"{int(total_engagement):,}")

st.markdown("---")

# ---------------------------
# ENGAGEMENT BY STATE
# ---------------------------

state_engagement = (
    filtered_df.groupby("State")["Engagement"]
    .sum()
    .reset_index()
    .sort_values("Engagement", ascending=False)
)

fig1 = px.bar(
    state_engagement,
    x="State",
    y="Engagement",
    title="Engagement by State"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------------------
# CONTENT PERFORMANCE
# ---------------------------

content_engagement = (
    filtered_df.groupby("ContentType")["Engagement"]
    .mean()
    .reset_index()
)

fig2 = px.bar(
    content_engagement,
    x="ContentType",
    y="Engagement",
    title="Average Engagement by Content Type"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------------------
# SENTIMENT DISTRIBUTION
# ---------------------------

sentiment_counts = {
    "Positive": (filtered_df["Total_Sentiment"] > 0).sum(),
    "Neutral": (filtered_df["Total_Sentiment"] == 0).sum(),
    "Negative": (filtered_df["Total_Sentiment"] < 0).sum()
}

sentiment_df = pd.DataFrame({
    "Sentiment": sentiment_counts.keys(),
    "Count": sentiment_counts.values()
})

fig3 = px.pie(
    sentiment_df,
    names="Sentiment",
    values="Count",
    title="Sentiment Distribution"
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------------------
# DAY-WISE ENGAGEMENT
# ---------------------------

day_engagement = (
    filtered_df.groupby("DateDay")["Engagement"]
    .sum()
    .reset_index()
)

fig4 = px.bar(
    day_engagement,
    x="DateDay",
    y="Engagement",
    title="Day-wise Engagement"
)

st.plotly_chart(fig4, use_container_width=True)

# ---------------------------
# LIKES DISTRIBUTION
# ---------------------------

fig5 = px.histogram(
    filtered_df,
    x="like_count",
    nbins=40,
    title="Likes Distribution"
)

st.plotly_chart(fig5, use_container_width=True)

# ---------------------------
# TOP POSTS
# ---------------------------

st.subheader("Top 20 Posts by Engagement")

top_posts = (
    filtered_df[
        ["State", "ContentType", "Status text", "Engagement"]
    ]
    .sort_values("Engagement", ascending=False)
    .head(20)
)

st.dataframe(top_posts, use_container_width=True)

# ---------------------------
# RAW DATA
# ---------------------------

with st.expander("View Dataset"):
    st.dataframe(filtered_df)