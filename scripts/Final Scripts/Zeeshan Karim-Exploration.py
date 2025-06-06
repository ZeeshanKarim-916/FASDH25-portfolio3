import pandas as pd

# Define the file paths for your CSV files
# Adjust these paths if your files are not in the same directory as your script

topic_model_filepath = ("../ topic-model/topic-model.csv")
length_filepath = ("../dataframes/length/length.csv")

# Load the dataset length
df_length = pd.read_csv(length_filepath)
print(df_length.head())
print(df_length.columns)

# Load the dataset topic modeling
df_topic_model = pd.read_csv(topic_model_filepath)
print(df_topic_model.head())
print(df_topic_model.columns)

# Data Merging 
# Merge the dataframes on common date columns (year, month, day)
df_merged = pd.merge(df_length, df_topic_model, on=['year', 'month', 'day'], how='inner')  #Code taken from Chatgpt, AI chat3


# Filter out rows where 'Topic' is -1 ---
df_filtered = df_merged[df_merged['Topic'] != -1]

print(df_filtered.head())
print(df_filtered.columns)

# Save the filtered dataframe to a CSV file 
# This will create a new CSV file named 'filtered_merged_data.csv' in the same directory
df_filtered.to_csv('filtered_merged_data.csv', index=False)

print("The filtered and merged dataframe has been saved as 'filtered_merged_data.csv'.")
print("You can now find this file in the same directory where you run this script.")

#Load the filtered and merged dataframe
df_filtered = pd.read_csv('filtered_merged_data.csv')

# Create a mapping of Topic ID to a Topic Name
# Convert 'Topic' to string first, as it might be numeric
df_filtered['Topic'] = df_filtered['Topic'].astype(str) #Code help taken from Chatgpt. AI chat solution 1.

# Get unique topics and their representative keywords
topic_keywords_df = df_filtered[['Topic', 'topic_1', 'topic_2', 'topic_3', 'topic_4']].drop_duplicates(subset=['Topic']).copy() #Code help taken from Slide DHFAS 15.1.

# Create a new column 'Topic_Name' by combining the top keywords
# Handle potential NaN values in topic_1, topic_2, topic_3 by converting to string first #Code help taken from Chatgpt. AI chat solution 1
topic_keywords_df['Topic_Name'] = topic_keywords_df['topic_1'].astype(str) + ', ' + \
                                   topic_keywords_df['topic_2'].astype(str) + ', ' + \
                                   topic_keywords_df['topic_3'].astype(str)

# Create a dictionary mapping numerical Topic ID (as string) to its new Topic_Name   #Code help taken from ChatGpt AI chat 2.
topic_id_to_name_map = dict(zip(topic_keywords_df['Topic'], topic_keywords_df['Topic_Name']))

print("Generated Topic ID to Name Mapping:")
for topic_id, topic_name in topic_id_to_name_map.items():
    print(f"Topic {topic_id}: {topic_name}")

#Step 2: Apply this mapping to the df_filtered dataframe
# This will add a 'Topic_Name' column to our main filtered dataframe
df_filtered['Topic_Name'] = df_filtered['Topic'].map(topic_id_to_name_map) #Code help taken from Assignment 14.2 in python exercises.

# Filter out rows where Topic_Name might be NaN (e.g., if some Topic IDs were not mapped)
df_filtered = df_filtered.dropna(subset=['Topic_Name']).copy()


# Filter data for years 2023 and 2024 and for the selected topics
# Modified filter condition to include both 2023 and 2024
df_filtered_2023_2024 = df_filtered[df_filtered['year'].isin([2023, 2024])].copy() #Code taken from SLide DHFAS 13.1

# Filter for the specific topics
selected_topic_ids = ['5', '76', '15', '77', '35']  #Code help taken from Slide DHFAS 13.1
df_filtered_selected_topics_2023_2024 = df_filtered_2023_2024[df_filtered_2023_2024['Topic'].isin(selected_topic_ids)].copy() #Code taken from Slide DHFAS 13.
print(df_filtered_selected_topics_2023_2024)
df_filtered_selected_topics_2023_2024.to_csv('df_filtered_selected_topics_2023_2024.csv', index=False)

