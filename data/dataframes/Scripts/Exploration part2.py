# === Import necessary libraries ===
import pandas as pd
import plotly.express as px

# === Step 1: Load the topic model data ===
topic_model_path = r'C:\Users\Admin\Downloads\FASDH25-portfolio3\data\dataframes\topic-model\topic-model.csv'
topic_df = pd.read_csv(topic_model_path)

# === Step 2: Remove unassigned topics (-1) ===
topic_df = topic_df[topic_df["Topic"] != -1].copy()

# === Step 3: Combine the four topic keywords into a readable label ===
topic_df["Label"] = topic_df[["topic_1", "topic_2", "topic_3", "topic_4"]].agg(', '.join, axis=1)
topic_df["Topic_Label"] = topic_df["Topic"].astype(str) + ": " + topic_df["Label"]

# === Step 4: Combine topic keywords into one lowercase string column for keyword matching ===
topic_df["all_keywords"] = topic_df["Label"].str.lower()

# === Step 5: Define thematic keyword groups for classification ===
military_keywords = [
    "airstrikes", "bombardment", "shelling", "ceasefire", "rockets",
    "clashes", "drones", "tanks", "military operation"
]

humanitarian_keywords = [
    "casualties", "wounded", "hospitals", "humanitarian", "displacement",
    "un", "children", "aid", "famine", "refugees"
]

diplomatic_keywords = [
    "ceasefire talks", "un resolution", "annexation", "statehood", "borders",
    "negotiations", "diplomatic pressure", "international condemnation"
]

# === Step 6: Create a 'month' column for temporal grouping ===
topic_df["month"] = pd.to_datetime(topic_df[["year", "month", "day"]], errors='coerce').dt.to_period("M").astype(str)

# === Step 7: Classify each topic into a thematic group based on keyword matching ===
def classify_group(keywords):
    if any(kw in keywords for kw in military_keywords):
        return "Conflict & Military Action"
    elif any(kw in keywords for kw in humanitarian_keywords):
        return "Civilian & Humanitarian Impact"
    elif any(kw in keywords for kw in diplomatic_keywords):
        return "Political & Diplomatic Response"
    else:
        return None  # Exclude topics that don’t match any group

topic_df["Group"] = topic_df["all_keywords"].apply(classify_group)

# === Step 8: Keep only relevant, classified groups for analysis ===
relevant_df = topic_df[topic_df["Group"].notnull()].copy()

# === Step 9: Group data by month and thematic group, and count articles per category ===
grouped_counts = relevant_df.groupby(["month", "Group"]).size().reset_index(name="Count")

# === Step 10 (NEW): Sort the months chronologically for proper time-series visualization ===
grouped_counts["month"] = pd.to_datetime(grouped_counts["month"])
grouped_counts = grouped_counts.sort_values("month")
grouped_counts["month"] = grouped_counts["month"].dt.to_period("M").astype(str)

# === Step 11: Visualize the trends using a grouped bar chart ===
fig = px.bar(
    grouped_counts,
    x="month",
    y="Count",
    color="Group",
    barmode="group",
    title="Conflict, Humanitarian, and Diplomatic Topic Trends Over Time",
    labels={
        "month": "Month",
        "Count": "Number of Articles",
        "Group": "Topic Group"
    }
)

# === Step 12: Save and display the interactive chart ===
fig.write_html("conflict_humanitarian_diplomatic_trends.html")
fig.show()
