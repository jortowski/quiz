''' This is a quiz app with streamlit

'''
import streamlit as st
import pandas as pd
import random

from google.oauth2 import service_account
from gsheetsdb import connect

# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)

# Perform SQL query on the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
#@st.cache_data(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

sheet_url = st.secrets["private_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')

st.write(rows)


df = pd.DataFrame(rows)
st.write(df["Autor"])

'''
def load_excel(file_path):
    df = pd.read_excel(file_path)
    return(df)

def shuffle_answers(row):
    correct_answer = row["Respuesta correcta"]
    fake_answer1 = row["Respuesta falsa 1"]
    fake_answer2 = row["Respuesta falsa 2"]
    answers = [correct_answer, fake_answer1, fake_answer2]
    random_answers = answers
    random.shuffle(random_answers)
    return(random_answers)

st.title("HAZ OTRO TEST!")

pwd = st.sidebar.text_input('Password:', value='', type='password')
if pwd == "Seaprueba":
    
    window_path = 'C:/Users/C79296/OneDrive - Canal de Isabel II/ICCP/'
    file_name = 'testing_test.xlsx'
    file_path = window_path + file_name
    
    df = load_excel(file_path)
    
    all_modules = df["Módulo"].drop_duplicates()
    all_authors = df["Autor"].drop_duplicates()
    
    with st.sidebar.form("filters"):
        st.header("Exam options")
        modules = st.multiselect('Módulos: ', all_modules, default=all_modules)
        authors = st.multiselect('Autores: ', all_authors, default=all_authors)
        df_filtered = df[df["Autor"].isin(authors) & df["Módulo"].isin(modules)]
        nrows = len(df_filtered)
        number_of_questions = st.number_input('Número de preguntas: ', min_value=0, max_value=nrows)
        filtered = st.form_submit_button("Start a test")
    
    if filtered:
        st.session_state['nq']=number_of_questions
        st.session_state['df_filtered'] = df_filtered
        st.session_state['nrows'] = nrows
        random_ids = random.sample(range(0, st.session_state.nrows), st.session_state.nq) 
        st.session_state['ids'] = random_ids
        
        questions = []
        answers = []
        correct_answers = []
    
        for i in st.session_state.ids:
            row=[df_filtered.iloc[i]][0]
            question = row["Pregunta"]
            correct_answer = row["Respuesta correcta"]
            random_answers = shuffle_answers(row)
            questions.append(question)
            answers.append(random_answers)
            correct_answers.append(correct_answer)
            
        st.session_state['questions']=questions
        st.session_state['answers']=answers 
        st.session_state['correct_answers']=correct_answers    

if 'questions' not in st.session_state:
    
    st.header('Introduce la contraseña y filtra las opciones de examen')

else:
    with st.form("quiz"):
        selected_answers = []
        for q in range(0,st.session_state.nq):
            selected_answers.append(st.radio(st.session_state.questions[q],st.session_state.answers[q]))
        submitted = st.form_submit_button("Submit")
    
    if submitted:
        st.session_state['selected_answers'] = selected_answers
        incorrect_answers = 0
        st.subheader('Has fallado estas preguntas:')
        for i in range(st.session_state.nq):
            correct = st.session_state.correct_answers[i][:]
            selected = st.session_state.selected_answers[i][:]
            if correct != selected:
                incorrect_answers +=1
                st.write(st.session_state.questions[i][:])
                st.write('Respuesta correcta: '+correct)
                st.write('Respuesta seleccionada: '+selected)
    
        mark=(st.session_state.nq - incorrect_answers)/st.session_state.nq*100
        st.title('Resultado: '+str("{:.2f}".format(mark))+' %')
      
    
 '''
    






