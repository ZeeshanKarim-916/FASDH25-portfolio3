import pandas as pd
import plotly.express as px

# Load the topic model dataframe
topic_model_path = r'C:\Users\Admin\Downloads\FASDH25-portfolio3\data\dataframes\topic-model\topic-model.csv'
topic_df = pd.read_csv(topic_model_path)

# Show first few rows of the dataframe
print("First 5 rows of the data:")
print(topic_df.head())

# Check unique years and months
print("\nUnique years:")
print(topic_df['year'].unique())
print("\nUnique months:")
print(topic_df['month'].unique())

# Step 2: Remove unassigned topics (-1)
topic_df = topic_df[topic_df["Topic"] != -1]


#Step 3: Find the 5 most common topics ===
top_5_topic_numbers = topic_df['Topic'].value_counts().head(5).index.tolist()

#Step 4: Filter to only top 5 topics ===
filtered_topic_df = topic_df[topic_df['Topic'].isin(top_5_topic_numbers)].copy()

#Step 5: Create readable topic labels ===
topic_labels = topic_df[['Topic', 'topic_1', 'topic_2', 'topic_3', 'topic_4']].drop_duplicates().copy()
topic_labels['Label'] = topic_labels[['topic_1', 'topic_2', 'topic_3', 'topic_4']].agg(', '.join, axis=1)
topic_labels['Topic_Label'] = topic_labels['Topic'].astype(str) + ": " + topic_labels['Label']

#Step 6: Merge topic labels with filtered data ===
filtered_topic_df = filtered_topic_df.merge(topic_labels[['Topic', 'Topic_Label']], on='Topic', how='left')

# Step 7: Create 'month' column
filtered_topic_df["month"] = pd.to_datetime(filtered_topic_df[["year", "month", "day"]], errors='coerce').dt.to_period("M").astype(str)

# Step 8: Group for line plot
monthly = filtered_topic_df.groupby(["month", "Topic_Label"]).size().reset_index(name="Count")

# Visualization 1: Plot as a facet grid (line plot) ===
fig = px.line(
    monthly,
    x="month",
    y="Count",
    facet_col="Topic_Label",
    facet_col_wrap=3,  # Number of charts per row
    title="Monthly Trends for Top 5 Topics (Facet Grid)",
    labels={"month": "Month", "Count": "Number of Articles", "Topic_Label": "Topic"}
)

fig.update_layout(height=600, width=1000)
fig.show()

# Step 9: Create a bar plot for monthly counts for Top 5 topics ===
fig = px.bar(
    monthly,
    x="month",
    y="Count",
    color="Topic_Label",
    barmode="group",
    title="Monthly Trends for Top 5 Topics (Bar Plot)",
    labels={"month": "Month", "Count": "Number of Articles", "Topic_Label": "Topic"}
)

fig.write_html("top_5_topics_monthly_barplot.html")
# export the chart to an HTML file so it can be viewed in a browser
fig.write_html("Zeeshan-karim-topicmodel-bar.html")
fig.show()

