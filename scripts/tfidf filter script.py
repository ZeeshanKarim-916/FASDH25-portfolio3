import pandas as pd
import plotly.express as px

df=pd.read_csv ('data/dataframes/tfidf/tfidf-over-0.3.csv')

filtered_df = df[(df['similarity'] <= 0.45)]

filtered_df.to_csv('tfidf_scores_less_than_0.45.csv', index=False)

