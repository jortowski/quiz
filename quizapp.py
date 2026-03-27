import streamlit as st
import pandas as pd
import random
import gspread
from google.oauth2.service_account import Credentials


# ===========================
#  1. CONECTAR A GOOGLE SHEETS
# ===========================

# Crear credenciales desde secrets.toml
credentials = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)

gc = gspread.authorize(credentials)

# URL de la hoja desde secrets
sheet_url = st.secrets["gsheets"]["private_gsheets_url"]

# Abrir hoja (funciona con URL)
sh = gc.open_by_url(sheet_url)
worksheet = sh.sheet1

# Obtener datos como lista de diccionarios
data = worksheet.get_all_records()
df = pd.DataFrame(data)



# ===========================
#  2. FUNCIONES
# ===========================

def shuffle_answers(row):
    """Mezcla respuestas incluyendo la correcta y las falsas"""
    answers = [
        row["Respuesta_correcta"],
        row["Respuesta_falsa_1"],
        row["Respuesta_falsa_2"],
    ]
    random.shuffle(answers)
    return answers



# ===========================
#  3. INTERFAZ STREAMLIT
# ===========================

st.title("HAZ OTRO TEST!")

pwd = st.sidebar.text_input('Password:', value='', type='password')

if pwd == "Seaprueba":

    all_modules = df["Módulo"].drop_duplicates()
    all_authors = df["Autor"].drop_duplicates()

    with st.sidebar.form("filters"):
        st.header("Exam options")
        modules = st.multiselect('Módulos: ', all_modules, default=all_modules)
        authors = st.multiselect('Autores: ', all_authors, default=all_authors)

        # Filtrado (OJO: corregido el operador &)
        df_filtered = df[df["Autor"].isin(authors) & df["Módulo"].isin(modules)]

        nrows = len(df_filtered)
        number_of_questions = st.number_input(
            'Número de preguntas:',
            min_value=1,
            max_value=nrows
        )

        filtered = st.form_submit_button("Start a test")

    if filtered:

        st.session_state['nq'] = number_of_questions
        st.session_state['df_filtered'] = df_filtered
        st.session_state['nrows'] = nrows

        random_ids = random.sample(range(0, nrows), number_of_questions)
        st.session_state['ids'] = random_ids

        questions = []
        answers = []
        correct_answers = []

        for i in random_ids:
            row = df_filtered.iloc[i]

            questions.append(row["Pregunta"])
            answers.append(shuffle_answers(row))
            correct_answers.append(row["Respuesta_correcta"])

        st.session_state['questions'] = questions
        st.session_state['answers'] = answers
        st.session_state['correct_answers'] = correct_answers



# ===========================
#  4. FORMULARIO DEL QUIZ
# ===========================

if "questions" not in st.session_state:

    st.header('Introduce la contraseña y filtra las opciones de examen')

else:

    with st.form("quiz"):
        selected_answers = []
        for i in range(st.session_state['nq']):
            selected = st.radio(
                st.session_state['questions'][i],
                st.session_state['answers'][i]
            )
            selected_answers.append(selected)

        submitted = st.form_submit_button("Submit")

    if submitted:

        st.session_state['selected_answers'] = selected_answers
        incorrect_answers = 0

        st.subheader("Has fallado estas preguntas:")

        for i in range(st.session_state['nq']):
            correct = st.session_state['correct_answers'][i]
            selected = st.session_state['selected_answers'][i]

            if correct != selected:
                incorrect_answers += 1
                st.write(st.session_state['questions'][i])
                st.write("✅ Respuesta correcta: " + correct)
                st.write("❌ Tu respuesta: " + selected)

        mark = (st.session_state['nq'] - incorrect_answers) / st.session_state['nq'] * 100
        st.title("Resultado: " + "{:.2f}".format(mark) + " %")









