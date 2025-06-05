import pandas as pd
import plotly.express as px
import os

# === Define file paths ===
tfidf_path = r'C:\Users\Admin\Downloads\FASDH25-portfolio3\data\dataframes\tfidf-over-0.3.csv'
topic_path = r'C:\Users\Admin\Downloads\FASDH25-portfolio3\data\dataframes\topic-model.csv'


# === Load data ===
df_tfidf = pd.read_csv(tfidf_path)
df_topic = pd.read_csv(topic_path)

# === Merge topic info for both articles ===
df = pd.merge(df_tfidf, df_topic[['file', 'Topic', 'year', 'month', 'day']],
              left_on='filename-1', right_on='file', how='left') \
       .rename(columns={'Topic': 'Topic_1', 'year': 'year_1', 'month': 'month_1', 'day': 'day_1'}) \
       .drop(columns='file')

df = pd.merge(df, df_topic[['file', 'Topic']],
              left_on='filename-2', right_on='file', how='left') \
       .rename(columns={'Topic': 'Topic_2'}) \
       .drop(columns='file')

# === Filter: Only pairs within the same topic ===
df_same_topic = df[df['Topic_1'] == df['Topic_2']].copy()

# === Convert to datetime and extract month ===
df_same_topic['date'] = pd.to_datetime(df_same_topic[['year_1', 'month_1', 'day_1']], errors='coerce')
df_same_topic['month'] = df_same_topic['date'].dt.to_period('M').astype(str)

# === Group by month and calculate average similarity ===
monthly_avg = df_same_topic.groupby('month')['similarity'].mean().reset_index()

# === Plot bar chart ===
fig = px.bar(
    monthly_avg,
    x='month',
    y='similarity',
    title='Monthly Average Similarity of Articles Within the Same Topic',
    labels={'month': 'Month', 'similarity': 'Average Similarity'},
    text='similarity'
)

fig.update_layout(xaxis_tickangle=-45)
fig.show()
