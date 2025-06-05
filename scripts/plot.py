import pandas as pd
import plotly.express as px

df=pd.read_csv('data/dataframes/tfidf/tfidf_scores_less_than_0.45.csv')

fig1 = px.box(
    df,
    x='month-1',
    y='similarity',
    title='Distribution of TF-IDF Similarities Over Time for row 1',
    labels={'similarity': 'Similarity', 'month-1': 'Time (in months)'}
)

fig1.update_layout(xaxis_tickformat='%b %Y')
fig1.show()

fig2 = px.box(
    df,
    x='month-2',
    y='similarity',
    title='Distribution of TF-IDF Similarities Over Time for row 2',
    labels={'similarity': 'Similarity', 'month-2': 'Time (in months)'}
)

fig2.update_layout(xaxis_tickformat='%b %Y')
fig2.show()


