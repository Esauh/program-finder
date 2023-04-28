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


def disable_submit():
    st.session_state["disabled"] = True
    st.session_state["listings"] = False


def enable_submit():
    st.session_state["disabled"] = False
    st.session_state["listings"] = True
    st.session_state["program_time"] = ""
    st.session_state["program_type"] = ""
    st.session_state["program_date"] = ""

if "disabled" not in st.session_state:
    st.session_state["disabled"] = False

if "listings" not in st.session_state:
    st.session_state["listings"] = True


st.markdown("# Setup :blue[Wizard] :mage:")
st.write("##")
with st.container():
    left_column, right_column = st.columns([3,1.5],gap="small")
    with left_column:
        with st.form(key="Question_Form"):
            st.markdown("### Please select the answer to all of the questions below then hit the :orange[Submit] button")
            st.divider()
            program_time = st.radio("# Would you want your child to do this activity during the school year or duing the summer?",
                                    ('Summer','School Year'))
            program_day = st.radio("# Would your child be available during the weekdays or weekends to participate in the program?",
                                ('Weekdays','Weekends'))
            program_type = st.radio("# What category would you like your child to excel and develop in?"
                                    ,('STEM','Fine Arts','Foreign Language'))
            submitted = st.form_submit_button(":orange[Submit]", on_click=disable_submit, disabled=st.session_state["disabled"])
            if submitted:
                st.success("Wizard Setup Complete", icon="✅")   
                st.balloons()   
                st.session_state["program_time"] = program_time
                st.session_state["program_type"] = program_type
                st.session_state["program_date"] = program_day
        st.write("##")
        with right_column:
            st_lottie(lottie_wand, height=650, width=650)
        with st.container():
            left_row, right_row = st.columns(2)
            with left_row:
                st.markdown("Click the :violet[Listings] button below to see all the programs found!")
                next_listings = st.button("Go To :violet[Listings]",use_container_width=True, disabled=st.session_state["listings"])
                if next_listings:
                    switch_page("listings")
            with right_row:
                st.markdown("Return to :green[Home] if you want!")
                return_home= st.button("Return :green[Home]",use_container_width=True) 
                if return_home:
                    switch_page("welcome")  

st.divider()
st.markdown("### If you wish to re-enter values for the setup wizard click this button which will allow you to :orange[Submit] again")
st.button("Reset :blue[Wizard]", on_click=enable_submit)
