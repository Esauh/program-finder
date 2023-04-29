import string
import streamlit as st 
from streamlit_extras.switch_page_button import switch_page
import psycopg2
from streamlit_lottie import st_lottie
import json

st.set_page_config(
    page_title="Program Listings",
    page_icon=":tada",
    initial_sidebar_state="collapsed",
    layout="wide"
)

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """

no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)
st.markdown(hide_menu_style, unsafe_allow_html=True)

def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

# Perform query.
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

if "program_type" not in st.session_state:
    st.session_state["program_type"] = "STEM"

if "program_time" not in st.session_state:
    st.session_state["program_time"] = "School Year"
    
if "program_date" not in st.session_state:
    st.session_state["program_date"] = "Weekends"


if st.session_state["program_time"] == "Summer":
    query_pt = 'Summer'
else:
    query_pt = 'School Year'

if st.session_state["program_date"] == "Weekend":
    query_pd = 'Weekends'
else:
    query_pd = 'Weekdays'

if st.session_state["program_type"] == "STEM":
    query_ptype = 'STEM'
elif st.session_state["program_type"] == "Fine Arts":
    query_ptype = 'Fine Arts'
elif st.session_state["program_type"] == "Foreign Language":
    query_ptype = 'Foreign Language'

program = "programs2"
query = f"select * from {program} where program_type ='{query_ptype}'  and program_date ='{query_pd}' and program_time ='{query_pt}';"

rows = run_query(query)

query_ptype = st.session_state["program_type"]

if query_ptype == "STEM":
    lottie = load_lottiefile("lottiefiles/coding.json")
elif query_ptype == "Fine Arts":
    lottie = load_lottiefile("lottiefiles/fine_arts.json")
else:
    lottie = load_lottiefile("lottiefiles/foreign_language.json")

st.markdown(f"### Here are some :violet[{query_ptype}] based programs click the name to view their website :raised_hands:")
st.divider()

with st.container():
    left_column, right_column = st.columns([2,3],gap="large")
    rank = 1
    with left_column:
        for row in rows:
            st.markdown(f"""
            ## :violet[Program {rank}:] [{row[6]}]({row[4]})
            ### :orange[Costs: ${row[5]}]
            """)
            st.divider()
            rank += 1
    with right_column:
        st_lottie(lottie, height=800, width=800)


#row[1] = School Year or Summer
#row[2] = Weekdays or Weekends
#row[3] = Stem or Foreign Language or Fine Arts
#row[4] = Website link
#row[5] = Cost of program
#row[6] = Name of program

with st.container():
    st.write("##")
    st.write("##")
    st.divider()
    right_column, left_column = st.columns(2)
    with left_column:

        return_wizard = st.button("Return to :blue[Wizard]", use_container_width=True)
        if return_wizard:
            switch_page("wizard")
    with right_column:
        return_home = st.button("Return :green[Home]", use_container_width=True)
        if return_home:
            switch_page("welcome")
    
