import pandas as pd

# Load Dataset
df = pd.read_csv("Data LIWC 01 02 23.csv")

print("\nDataset Shape")
print(df.shape)

print("\nColumns")
print(df.columns.tolist())

# Create Engagement Metric
df["Engagement"] = (
    df["like_count"]
    + df["retweet_count"]
    + df["reply_count"]
    + df["quote_count"]
)

print("\nSummary Statistics")
print(df[[
    "like_count",
    "retweet_count",
    "reply_count",
    "quote_count",
    "Followers",
    "Buzz",
    "Engagement"
]].describe())

print("\nTop 10 States by Engagement")

top_states = (
    df.groupby("State")["Engagement"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print(top_states)

print("\nTop Content Types")

content = (
    df.groupby("ContentType")["Engagement"]
    .mean()
    .sort_values(ascending=False)
)

print(content)

print("\nSentiment Summary")

print(df["Total_Sentiment"].describe())

print("\nAnalysis Completed Successfully")