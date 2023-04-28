import string
import streamlit as st 
from streamlit_extras.switch_page_button import switch_page
import psycopg2

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

st.session_state
@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()
    
st.header("Program :red[Listings]!")

query_pt = st.session_state["program_time"]
query_pd = st.session_state["program_date"]
query_ptype = st.session_state["program_type"] 

if st.session_state["program_time"] == "Summer":
    query_pt = 'Summer'
else:
    query_pt = 'School Year'

if st.session_state["program_date"] == "Weekend":
    query_pd = 'Weekend'
else:
    query_pd = 'Weekday'

if st.session_state["program_type"] == "STEM":
    query_ptype = 'STEM'
elif st.session_state["program_type"] == "Fine Arts":
    query_ptype = 'Fine Arts'
elif st.session_state["program_type"] == "Foreign Language":
    query_ptype = 'Foreign Language'

rows = run_query("SELECT * FROM Program WHERE program_time =" + query_pt + " and program_date = " + query_pd + " and program_type = " + query_ptype + ";")

# Print results.
for row in rows:
    st.write(f"{row[1]} has a {row[2], {row[3]}} {row[4]}:")

with st.container():
    st.write("##")
    st.write("To return :green[Home] below")
    return_home = st.button("Return :green[Home]")
    if return_home:
        switch_page("welcome")
