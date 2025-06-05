import pandas as pd

csv_path='data/dataframes/tfidf/tfidf-over-0.3.csv'
df=pd.read_csv(csv_path)

df1=df[['filename-1', 'filename-2','similarity']].copy()
edges=df1.rename(columns={
    'filename-1' : 'Source',
    'filename-2' : 'Target',
    'similarity' : 'Weight'})
 
print (edges.head(2))

node1=df[['filename-1','title-1','month-1']].copy()
node1=node1.rename(columns={
    'filename-1':'Id',
    'month-1':'month',
    'title-1':'Label'})


node2=df[['filename-2','title-2','month-2']].copy()
node2=node2.rename(columns={
    'filename-2':'Id',
    'month-2':'month',
    'title-2':'Label'})

node1=node1[['Id','Label','month']]
node2=node2[['Id','Label','month']]

nodes=pd.concat([node1, node2])
nodes=nodes.drop_duplicates(subset='Id')

print (nodes.head(2))

edges.to_csv ('data/dataframes/tfidf/outputs/Shaharyar_amin-edges-over-0.3.csv', encoding= 'utf-8-sig',index=False)
nodes.to_csv ('data/dataframes/tfidf/outputs/Shaharyar_amin-nodes-over-0.3.csv', encoding='utf-8-sig', index= False)

