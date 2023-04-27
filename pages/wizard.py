import streamlit as st 
from streamlit_extras.switch_page_button import switch_page
from streamlit_lottie import st_lottie
import json
st.set_page_config(
    page_title="Wizard Setup",
    page_icon=":page:",
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

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


st.title("ProgramFinder Wizard :mage:")
st.write("##")
with st.container():
    left_column, right_column = st.columns([1,1.5],gap="small")
    with left_column:
        with st.form("Question_Form"):
            st.subheader("Please select the correct answer to all of the questions below then hit the Submit button :raised_hands:")
            st.divider()
            program_time = st.radio("Would you want your child to do this activity during the school year or duing the summer?",
                                    ("Summer","School Year"))
            program_day = st.radio("Would your child be available during the weekdays or weekends to participate in the program?",
                                ("Weekdays","Weekends"))
            program_type = st.radio("What category would you like your child to excel and develop in?"
                                    ,('STEM','Fine Arts','Foreign Language'))
            submitted = st.form_submit_button("Submit Answers")
            if submitted:
                st.write()
                
    
