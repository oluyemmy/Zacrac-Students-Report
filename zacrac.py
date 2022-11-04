import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from PIL import Image
import plotly.express as px

image = Image.open('logo-icon.png')

st.image(image, width = 120, caption='Zacrac learning')
st.title("Zacrac Students Progress Report")
st.markdown(""" This app performs simple class reporting for all currently enrolled Zacrac Learning students!
* **Tracks:** Incubator cohorts, Excel Physical cohort, Pyhton hybrid cohort.
* **Data source:** [zacrac-grading-sheet.com](https://docs.google.com/spreadsheets/d/1jpTmWZXy2oo5EKKK75EBqReCFHjEkJGKdMXlbQLvxIE/).
""")
#### Select Track 
st.sidebar.header('Select Tracks')
selected_track = st.sidebar.selectbox('Learning tracks',['Python incubator','Powerbi incubator','Excel September Cohort'])

def load_data(track):
    df= pd.read_excel(io='zacrac_grading_sheet.xlsx',sheet_name = track)
    df_drop = df.drop('S/N', axis=1)
    return df_drop
trackselected = load_data(selected_track)

#### Select Cohort 

st.sidebar.header('Select student name')
selected_python_student_name = st.sidebar.selectbox('Python Cohort',
                                                    ['Tomisin Falode','Akinmutimi Gbemiro','Adedara David','Blessing Okeke',
'Moronke Rachael','Ayeni funmilayo','Dada Jasmine','Christopher Afolabi','Koyejo Dada Kay','Hagbolahan Tosin '])

selected_powerbi_student_name = st.sidebar.selectbox('Powerbi Cohort',
                                                    ['Lanre Adeyemo','Nchelem Anita','Temitope Boluwatife','Adeleke Kafayat',
 'Ajibola Majeed','Gbore Oluwaseun Daniel','Ugbong Paul','Oluwasegun Onimisi'])

selected_excel_student_name = st.sidebar.selectbox('Excel Physical Cohort',
                                                    ['Aderonke Olagunju','Favour Oyetunde','Jaiyeoba Oluwayimika','Ojenike Adekemi',
'Ola Timilehin','Tolulope Henry'])

#### Filtering data 
df_select_name = trackselected['Name']
df_select_total = trackselected['Total']
df_selected_class =trackselected[trackselected.columns.difference(['Name','Total'])].fillna(0)
df_selected_class.insert(0,'Name',df_select_name)
df_selected_class.insert(26,'Total',df_select_total)

st.header('Display cohort information of Selected Tracks')
st.write('Data Dimension: ' + str(df_selected_class.shape[0]) + ' rows and ' + str(df_selected_class.shape[1]) + ' columns.')
st.dataframe(df_selected_class.head(5))
### Download data
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="trackselected.csv">Download CSV File</a>'
    return href
st.markdown(filedownload(df_selected_class), unsafe_allow_html=True)

###Producing the visualization

st.header("Students Overall Performance")

fig = px.bar(df_selected_class, y=df_selected_class['Name'].dropna(),x=df_selected_class['Total'].dropna(),orientation='h',
            labels={'y':"Student names", "x": "Total"})

st.plotly_chart(fig)


### To select part of the dataset 
df2 = trackselected[['Aggreegate','Name', 'Week 1', 'Week 2', 'Week 3', 'Week 4',
       'Week 5', 'Week 6', 'Week 7', 'Week 8', 'Week 9', 'Week 10', 'Week 11',
       'Week 12', 'Week 13', 'Week 14', 'Week 15', 'Week 16', 'Week 17',
       'Week 18', 'Week 19', 'Week 20', 'Week 21', 'Week 22', 'Week 23',
       'Week 24']]

df_attendance_score= df2.set_index('Aggreegate').T['Attendance Score']

df_attendance_score.columns = df_attendance_score.loc['Name'].values

df_attendance_score.drop('Name', inplace = True)
df_attendance_score.fillna(0, inplace = True)

##Plot the attendance
st.header('Average Attendance Score by Students')
a_score = pd.DataFrame(df_attendance_score.mean(),columns=['Average']).reset_index()
fig = px.line(a_score, y= 'Average', x = 'index', labels={"index": "Names"})

st.plotly_chart(fig)

##Plot theAssignment performance
df_assignment_score= df2.set_index('Aggreegate').T['Assignment/Classwork']
df_assignment_score.columns = df2['Name'].dropna().values
df_assignment_score.drop('Name', inplace = True)
df_assignment_score.fillna(0, inplace = True)
b_score = pd.DataFrame(df_assignment_score.mean(),columns=['Average']).reset_index()
st.header('Average Performance Score by Students')
fig = px.line(b_score, y= 'Average', x = 'index', labels={"index": "Names"})
st.plotly_chart(fig)

### Students by Students Aggregate
df_assignment_score.index = range(1,25)
df_attendance_score.index = range(1,25)

###defining function for the python plot
def plot_grade(x):
    plt.style.use('seaborn')
    plt.subplot(1,2,1)
    plt.plot(df_assignment_score[x], 'b')
    plt.title('{} assignment report'.format(x))
    plt.xlabel('Weeks')
    plt.ylabel('Score')
    plt.xticks([0,5,10,15,20,25],['w0','w5','w10','w15','w20','w25'])
    plt.subplot(1,2,2)
    plt.plot(df_attendance_score[x],'r')
    plt.title('{} attendance report'.format(x))
    plt.xlabel('Weeks')
    plt.ylabel('Score')
    plt.xticks([0,5,10,15,20,25],['w0','w5','w10','w15','w20','w25'])
    plt.tight_layout()
st.header('Python Students weekly report')
f, ax = plt.subplots(figsize=(10,4)) 
ax= plot_grade(selected_python_student_name)
st.pyplot(f)

