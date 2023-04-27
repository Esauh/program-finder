import streamlit as st 
from streamlit_extras.switch_page_button import switch_page
from streamlit_lottie import st_lottie
import json
st.set_page_config(
    page_title="Wizard Setup",
    page_icon=":mage:",
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

lottie_wand = load_lottiefile('lottiefiles/magic-wand.json')

def disable():
    st.session_state.disabled = True

if "disabled" not in st.session_state:
    st.session_state.disabled=False

st.markdown("# Setup :blue[Wizard] :mage:")
st.write("##")
with st.container():
    left_column, right_column = st.columns([2,1.5],gap="small")
    with left_column:
        with st.form("Question_Form"):
            st.markdown("### Please select the answer to all of the questions below then hit the :green[Submit] button")
            st.divider()
            if "visibility" not in st.session_state:
                st.session_state.disabled = False
            program_time = st.radio("Would you want your child to do this activity during the school year or duing the summer?",
                                    ("Summer","School Year"))
            program_day = st.radio("Would your child be available during the weekdays or weekends to participate in the program?",
                                ("Weekdays","Weekends"))
            program_type = st.radio("What category would you like your child to excel and develop in?"
                                    ,('STEM','Fine Arts','Foreign Language'))
            #TODO:disable functionality is not working
            submitted = st.form_submit_button("Submit", on_click=disable, disabled=st.session_state.disabled)
            if submitted:
                st.success("Wizard Setup Complete", icon="✅")   
                st.balloons()   
            st.write("##")
        with right_column:
            st_lottie(lottie_wand, height=650, width=650)
        with st.container():
            st.markdown("### After clicking :green[Submit] click the button below to see all the programs found if you entered the information in incorrectly return to home and nagivate back to the wizard :raised_hands:")
            left_row, right_row = st.columns(2)
            with left_row:
                next_listings = st.button("Go To Listings Page")
                if next_listings:
                    switch_page("listings")
            with right_row:
                return_home= st.button("Return Home") 
                if return_home:
                    switch_page("welcome")         
    
