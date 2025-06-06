#importing important libraries
import pandas as pd
import plotly.express as px 

#mimport stop words from NLTK to filter out common words
# got help from https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
import nltk
from nltk.corpus import stopwords

# downloading the stop watch list
nltk.download('stopwords')

# loading the list of stopwords (English)
stop_words = set(stopwords.words('english'))

#define path
csv_path = ("data/dataframes/n-grams/1-gram/1-gram-year-month.csv")

#read the csv file
df = pd.read_csv(csv_path)

# printing the first 50 rows to understand the structure 
print("first 20 rows:\n", df.head(50))

#Combine year and month into a proper date column for time-series plotting (14.1) 
df["date"] = pd.to_datetime(df[["year", "month"]].assign(day=1))

# removing the stop words from the data  
df = df[~df['1-gram'].isin(stop_words)]

# identiying the twenty most frequent unigrams 
top_words = (
    df.groupby('1-gram')['count-sum']
    .sum()
    .sort_values(ascending=False)
    .head(20)
)

print("\nTop 50 most frequent unigrams:\n")
print(top_words)

# Keep only rows where the 1-gram is in the top 50
top_words_list = top_words.index.tolist()
df_top = df[df['1-gram'].isin(top_words_list)]

# set the group fo date and unigram
df_grouped = df_top.groupby(['date', '1-gram'])['count-sum'].sum().reset_index()

# Plot using Plotly
fig = px.line(df_grouped, x='date', y='count-sum', color='1-gram',
              title='Monthly Usage of the Top 10 Unigrams in the al-Jazeera corpus',
              labels={'date': 'Month', 'count': 'Mentions', '1-gram': 'Word'})

#save and show the graph
fig.write_html("top20_unigrams_plot.html")
fig.show()
