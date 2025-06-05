import pandas as pd

# Define the file paths for your CSV files
# Adjust these paths if your files are not in the same directory as your script

topic_model_filepath = ("../dataframes/topic-model/topic-model.csv")
length_filepath = ("../dataframes/length/length-year-month.csv")

# Load the datasets
df_length = pd.read_csv(length_filepath)
df_topic_model = pd.read_csv(topic_model_filepath)

# Data Merging 
# Merge the dataframes on common date columns (year, month, day)
df_merged = pd.merge(df_length, df_topic_model, on=['year', 'month'], how='inner')

# Filter out rows where 'Topic' is -1 ---
df_filtered = df_merged[df_merged['Topic'] != -1]

# Save the filtered dataframe to a CSV file ---
# This will create a new CSV file named 'filtered_merged_data.csv' in the same directory
# where your Python script is executed.
df_filtered.to_csv('filtered_merged_data.csv', index=False)

print("The filtered and merged dataframe has been saved as 'filtered_merged_data.csv'.")
print("You can now find this file in the same directory where you run this script.")

# --- Start of new analysis: Keyword Length Correlation ---

# Initialize a dictionary to store lengths for each keyword
keyword_lengths = {}

# Iterate through each row of the filtered dataframe
for index, row in df_filtered.iterrows():
    length = row['length']
    # For each topic column, add the document length to the respective keyword's list
    # Use .get() to handle potential missing columns gracefully
    for col in ['topic_1', 'topic_2', 'topic_3', 'topic_4']:
        keyword = row.get(col)
        if pd.notna(keyword):  # Ensure keyword is not NaN
            if keyword not in keyword_lengths:
                keyword_lengths[keyword] = []
            keyword_lengths[keyword].append(length)

# Calculate the average length for each unique keyword
# Ensure that 'lengths' list is not empty before calculating mean to avoid division by zero
avg_length_by_keyword = {keyword: sum(lengths) / len(lengths) for keyword, lengths in keyword_lengths.items() if lengths}

# Convert the results to a pandas DataFrame for easier manipulation and sorting
df_avg_length_by_keyword = pd.DataFrame(avg_length_by_keyword.items(), columns=['Keyword', 'Average Length'])

# Sort the DataFrame by average length in descending order
df_avg_length_by_keyword = df_avg_length_by_keyword.sort_values(by='Average Length', ascending=False)

# Print the top 10 keywords by average document length
print("\n--- Keyword Length Analysis ---")
print("Top 10 Keywords by Average Document Length:")
print(df_avg_length_by_keyword.head(10).to_markdown(index=False, numalign="left", stralign="left"))
