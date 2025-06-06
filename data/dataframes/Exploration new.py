import pandas as pd

# Define the file paths for your CSV files
# Adjust these paths if your files are not in the same directory as your script

topic_model_filepath = ("../dataframes/topic-model/topic-model.csv")
length_filepath = ("../dataframes/length/length.csv")

# Load the datasets
df_length = pd.read_csv(length_filepath)
df_topic_model = pd.read_csv(topic_model_filepath)

# Data Merging 
# Merge the dataframes on common date columns (year, month, day)
df_merged = pd.merge(df_length, df_topic_model, on=['year', 'month', 'day'], how='inner')  #Code taken from Chatgpt, AI chat3

# Filter out rows where 'Topic' is -1 ---
df_filtered = df_merged[df_merged['Topic'] != -1]

# Save the filtered dataframe to a CSV file ---
# This will create a new CSV file named 'filtered_merged_data.csv' in the same directory
# where your Python script is executed.
df_filtered.to_csv('filtered_merged_data.csv', index=False)

print("The filtered and merged dataframe has been saved as 'filtered_merged_data.csv'.")
print("You can now find this file in the same directory where you run this script.")

