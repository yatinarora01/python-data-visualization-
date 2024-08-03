import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image


st.set_page_config(page_title = 'Survey Results')

st.header('Survey Results2021')
st.subheader('Was the tutorial helpful?')


#---load dataframe 

excel_file = 'Survey_results.xlsx'
sheet_name = 'DATA'

df = pd.read_excel(excel_file,
                   sheet_name = sheet_name,
                   usecols = 'B:D',
                   header=3)

df_participants = pd.read_excel(excel_file, 
                                sheet_name = sheet_name,
                                usecols = 'F:G',
                                header=3)

# df_participants.dropna(inPlace = True)

department = df['Department'].unique().tolist()
ages = df['Age'].unique().tolist()

age_selection = st.slider('Age:',
                          min_value = min(ages),
                          max_value = max(ages),
                          value =( min(ages),max(ages)))

department_selection = st.multiselect('Department : ',
                                      department,
                                      default=department)

# filter dataframe based on selection 

mask = (df['Age'].between(*age_selection)) & (df['Department'].isin(department_selection))

number_of_results = df[mask].shape[0]

st.markdown(f'*Available Results : {number_of_results}*')

df_grouped = df[mask].groupby(by=['Rating']).count()[['Age']]

df_grouped = df_grouped.rename(columns={'Age' : 'Votes'})

df_grouped = df_grouped.reset_index()


# --- plot bar chart

bar_chart = px.bar(df_grouped,
                   x = 'Rating',
                   y = 'Votes',
                   text = 'Votes',
                   color_discrete_sequence= ['#F63366'] * len(df_grouped),
                   template='plotly_white')

st.plotly_chart(bar_chart)


st.dataframe(df)

pie_chart = px.pie(df_participants,
                   title = 'Total No. of Participants',
                   values = 'Participants',
                   names = 'Departments')



st.plotly_chart(pie_chart)