# importing necessary libraries
import pandas as pd
import plotly.express as px

#define path
csv_path = ("data/dataframes/n-grams/1-gram/1-gram-year-month.csv")

#read the csv file
df = pd.read_csv(csv_path)

# Create 'date' column to understand monthly summaries(code from assigment of 13.1)
df['date'] = pd.to_datetime(df[['year', 'month']].assign(day=1))

#Filter conflict related words(two sets of words) 
Conflict_related_filter_list = ['attacks', 'casualties', 'strike', 'killed', 'military']
Peace_related_filter_list = ['peace', 'ceasefire', 'relief', 'aid', 'humanitarian']

# make a new list
all_words = Conflict_related_filter_list + Peace_related_filter_list

#filter the data frames to include only relevent n-gram(code taken from 14.1 session of class slides)
df = df[df['1-gram'].isin(all_words)]

# categorise the list (refrence ai documentation heading 2)
df['category'] = df['1-gram'].apply(
    lambda word: 'conflict' if word in Conflict_related_filter_list
    else 'peace'
)

# print the result
print(df)

# define the start and end date (heading 1 in ai documentation)
start_date = '2022-10-01'
end_date = '2024-10-01'
df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
print(df)

# adding month colum (heading 3 in ai documentation)
df['month'] = df['date'].dt.to_period('M')

#absolute frequency section
#sum counts by monthly and categorzise them
monthly_abs_freq = (
    df.groupby(['month', 'category'])['count-sum']
      .sum()
      .reset_index()
)

# converting period to string
monthly_abs_freq['month'] = monthly_abs_freq['month'].astype(str)

#plot the graph bar
fig_abs_bar = px.bar(
    monthly_abs_freq,
    x='month',
    y='count-sum',
    color='category',
    barmode='group',         
    text='count-sum',
    title='Absolute Frequency: Conflict vs Peace 1-gram Frequency by Month (Oct 2022 – Oct 2024)',
    labels={'month':'Month', 'count-sum':'Total Mentions'}
)

#plot the graph line
fig_abs_line = px.line(
    monthly_abs_freq,
    x='month',
    y='count-sum',
    color='category',         
    text='count-sum',         
    title='Absoulte Frequency Trend: Conflict vs Peace 1-gram Frequency by Month (Oct 2022 – Oct 2024)',
    labels={'month':'Month', 'count-sum':'Total Mentions'}
)

#Relative Frequency Section

#calculate the relative frequency(ai docuemnetation heading 4)
df['relative_freq'] = df['count-sum'] / df.groupby('date')['count-sum'].transform('sum')

# adding month colum (heading 3 in ai documentation)
df['month'] = df['date'].dt.to_period('M')

# use relative frequency by month and category 
monthly_relative_freq = (
    df.groupby(['month', 'category'])['relative_freq']
      .sum()
      .reset_index()           
)

# converting month to string for plotting 
monthly_relative_freq['month'] = monthly_relative_freq['month'].astype(str)


#plot the graph
fig_relative_bar = px.bar(
    monthly_relative_freq,
    x='month',
    y='relative_freq',
    color='category',
    barmode='group',                  
    title='Relative Frequency of Conflict vs Peace 1-gram Frequency by Month (Oct 2022 – Oct 2024)',
    labels={'month':'Month', 'relative_freq':'Relative Frequency'}
)
fig_relative_line = px.line(
    monthly_relative_freq,
    x='month',
    y='relative_freq',
    color='category',                  
    title='Relative Frequency of Conflict vs Peace 1-gram Frequency by Month (Oct 2022 – Oct 2024)',
    labels={'month':'Month', 'relative_freq':'Relative Frequency'}
)

#show the line and bar grpah 
fig_abs_bar.show()
fig_abs_line.show()
fig_relative_bar.show()
fig_relative_line.show()

#saving the files in HTML
fig_abs_bar.write_html("absolute_bar_chart.html")
fig_abs_line.write_html("absolute_line_chart.html")
fig_relative_bar.write_html("relative_bar_chart.html")
fig_relative_line.write_html("relative_line_chart.html")

                          

