import pandas as pd
import plotly.express as px

# Load the filtered and merged dataframe
df_filtered = pd.read_csv('filtered_merged_data.csv')

# --- Start of User's Provided Topic Naming Logic (Reused) ---
# Create a mapping of Topic ID to a Topic Name
# Convert 'Topic' to string first, as it might be numeric
df_filtered['Topic'] = df_filtered['Topic'].astype(str)

# Get unique topics and their representative keywords
topic_keywords_df = df_filtered[['Topic', 'topic_1', 'topic_2', 'topic_3', 'topic_4']].drop_duplicates(subset=['Topic']).copy()

# Create a new column 'Topic_Name' by combining the top keywords
# Handle potential NaN values in topic_1, topic_2, topic_3 by converting to string first
topic_keywords_df['Topic_Name'] = topic_keywords_df['topic_1'].astype(str) + ', ' + \
                                   topic_keywords_df['topic_2'].astype(str) + ', ' + \
                                   topic_keywords_df['topic_3'].astype(str)

# Create a dictionary mapping numerical Topic ID (as string) to its new Topic_Name
topic_id_to_name_map = dict(zip(topic_keywords_df['Topic'], topic_keywords_df['Topic_Name']))

# Apply this mapping to the df_filtered dataframe
df_filtered['Topic_Name'] = df_filtered['Topic'].map(topic_id_to_name_map)

# Filter out rows where Topic_Name might be NaN (e.g., if some Topic IDs were not mapped)
df_filtered = df_filtered.dropna(subset=['Topic_Name']).copy()
# --- End of User's Provided Topic Naming Logic ---

# --- Visualization 1: Article Length Distribution by Topic ---
# Create a box plot to show the distribution of article lengths for each topic name
fig_length_by_topic = px.box(df_filtered,
                             x='Topic_Name',
                             y='length',
                             title='Distribution of Article Lengths by Topic',
                             labels={'Topic_Name': 'Topic', 'length': 'Article Length (Number of Words)'},
                             hover_data={'length': True, 'Topic_Name': True}
                            )

# Customize layout for better readability
fig_length_by_topic.update_layout(
    xaxis_title="Topic",
    yaxis_title="Article Length (Number of Words)",
    font=dict(family="Inter", size=12),
    margin=dict(l=40, r=40, t=80, b=100), # Adjust bottom margin for long topic names
    xaxis={'categoryorder':'total descending'} # Order topics by median length or total count for better insights
)

# Rotate x-axis labels if they are too long
fig_length_by_topic.update_xaxes(tickangle=45)

# Save the figure
fig_length_by_topic.write_html("article_length_by_topic_boxplot.html")

# Show the plot
fig_length_by_topic.show()
