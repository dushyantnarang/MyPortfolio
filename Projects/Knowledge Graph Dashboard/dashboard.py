import pandas as pd
from datetime import datetime
import streamlit as st
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

concepts = pd.read_csv('E:\Datasets\kg_data\dashboard\concept_data.csv')
competency = pd.read_csv('E:\Datasets\kg_data\dashboard\competency_data.csv')


concepts['date_created'] =  pd.to_datetime(concepts['created_at'], unit='s')
concepts = concepts.sort_values(by=['created_at'], ascending=False)
concepts.drop(['created_at'], axis='columns', inplace=True)
concepts['date_created'] = concepts['date_created'].dt.date

plot_concept = concepts.groupby(['date_created','created_by']).agg({"concept_id":"count"}).reset_index().sort_values(by=['date_created'], ascending=False)
plot_concept = plot_concept.rename(columns={"concept_id":"concept_count"})

st.title('Knowledge Graph Dashboard App')
st.text('This App shows KG Stats (Count of Entities Created Over Time)')
st.header('A closer look into the concept count data')

fig = go.Figure(data=go.Table(columnwidth=[3,3,2],
                    header=dict(values=list(plot_concept[['date_created','created_by','concept_count']].columns), fill_color = '#FD8E72', align='center'),
                    cells=dict(values=[plot_concept.date_created,plot_concept.created_by,plot_concept.concept_count], fill_color = '#E5ECF6', align='center')))
fig.update_layout(
    width=600,
    height=300,
    margin=dict(l=20,r=20,b=5,t=5))
st.write(fig)

st.header('No. of Concepts Created Over Time')
top_n = st.text_input('How many recent concept datapoints would you like to see?', 30)
top_n = int(top_n)
plot_concept = plot_concept.head(top_n)

kg_concept_graph = px.bar(plot_concept, 
        x='date_created',
        y='concept_count',
        text='concept_count',
        color='created_by')
kg_concept_graph.update_layout(
        showlegend=True,
        width=800,
        height=450,
        margin=dict(r=1,l=1,t=40,b=10),
        font=dict(size=12))
kg_concept_graph.update_xaxes(type='category')
st.write(kg_concept_graph)


competency.replace([np.inf, -np.inf], np.nan, inplace=True)
competency = competency.dropna(subset=["created_at", "created_by"], how="all")
competency['date_created'] =  pd.to_datetime(competency['created_at'], unit='s')
competency = competency.sort_values(by=['created_at'], ascending=False)
competency.drop(['created_at'], axis='columns', inplace=True)
competency['date_created'] = competency['date_created'].dt.date

plot_competency = competency.groupby(['date_created','created_by']).agg({"competency_id":"count"}).reset_index().sort_values(by=['date_created'], ascending=False)[:15]
plot_competency = plot_competency.rename(columns={"competency_id":"competency_count"})

st.header('No. of Competencies Created Over Time')
top_m = st.text_input('How many recent competency datapoints would you like to see?', 30)
top_m = int(top_m)
plot_competency = plot_competency.head(top_m)

kg_competency_graph = px.bar(
        plot_competency, 
        x='date_created',
        y='competency_count',
        text='competency_count',
        color='created_by')
kg_competency_graph.update_layout(
        showlegend=True,
        width=800,
        height=450,
        margin=dict(r=1,l=1,t=40,b=10),
        font=dict(size=12))
kg_competency_graph.update_xaxes(type='category')
st.write(kg_competency_graph)
