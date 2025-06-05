import pandas as pd
import plotly.express as px

df_filtered_selected_topics_2023_2024_filepath = ("../dataframes/df_filtered_selected_topics_2023_2024.csv")

# Load the datasets
df_filtered_selected_topics_2023_2024= pd.read_csv(df_filtered_selected_topics_2023_2024_filepath)


# Prepare data for plotting
# Creating a 'Year_Month' column for chronological ordering and clear X-axis labels
df_filtered_selected_topics_2023_2024['Year_Month'] = df_filtered_selected_topics_2023_2024['year'].astype(str) + '-' + \
                                                      df_filtered_selected_topics_2023_2024['month'].astype(str).str.zfill(2)

# Count occurrences of each Topic_Name per Year_Month
df_plot = df_filtered_selected_topics_2023_2024.groupby(['Year_Month', 'Topic_Name']).size().reset_index(name='Count')

# Ensure correct sorting in a proper order.
df_plot['Year_Month_Sort_Key'] = pd.to_datetime(df_plot['Year_Month'], format='%Y-%m')
df_plot = df_plot.sort_values(by='Year_Month_Sort_Key').drop(columns='Year_Month_Sort_Key')

#Visualization 1:
# Create the bar graph
fig = px.bar(df_plot,             #Code taken from slide DHFAS 15.1
             x='Year_Month',
             y='Count',
             color='Topic_Name',
             barmode='group', # This places bars for different topics side-by-side for each month
             title='Distribution of Selected Topics by Month (2023 & 2024)',
             labels={'Year_Month': 'Year-Month', 'Count': 'Number of Occurrences', 'Topic_Name': 'Topic'},
             hover_data={'Topic_Name': True, 'Count': True}
            )

# Customize the layout for better readability
fig.update_layout(
    xaxis_title="Year-Month",
    yaxis_title="Number of Occurrences",
    legend_title="Topic",
    hovermode="x unified", # Shows hover information for all bars at a given x-coordinate
    font=dict(family="Inter", size=12),
    margin=dict(l=40, r=40, t=80, b=40), # Adjust margins
    bargap=0.1, # Gap between bars of the same group
    bargroupgap=0.05 # Gap between groups of bars
)

#Visualization 2:
# Create a line graph
fig_line = px.line(df_plot,              #Code taken from Slide DHFAS 15.1
                   x='Year_Month',
                   y='Count',
                   color='Topic_Name',
                   markers=True,  # Adds points on the lines
                   title='Trend of Selected Topic Occurrences Over Time (2023 & 2024)',
                   labels={'Year_Month': 'Year-Month', 'Count': 'Number of Occurrences', 'Topic_Name': 'Topic'}
                  )

# Show the line graph
fig_line.show()

# Now save the figure
fig.write_html("Zeeshan-karim-topicmodel-bar.html") #code taken from Slide DHFAS 15.1

# Show the plot
fig.show()
