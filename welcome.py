import json
import streamlit as st 
from streamlit_extras.switch_page_button import switch_page
from streamlit_lottie import st_lottie

#Basic page setup for welcome page including lottie animations and hidden hamburger+nagivation menus must be first in every file
st.set_page_config(
    page_title="Welcome Page",
    page_icon=":tada",
    initial_sidebar_state="collapsed",
    layout = "wide"
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

lottie_graduation = load_lottiefile('lottiefiles/graduation.json')
lottie_search = load_lottiefile('lottiefiles/cloud-library.json')

with st.container():
    left_column, right_column = st.columns([3,1.5], gap="small")
    with left_column:
        st.title("Hi, welcome to ProgramFinder! :wave:")
        st.write("##")
        st.write("""This web app is to help parents and those who work with children find suitable high quality extra curricular education programs for students""")
        st.write(
        """
        There has been countless research showing student participation in afterschool or summer programs contribute to:
        - **Lowering school dropout**
        - **Raising enrollment into higher education**
        - **Increasing math, reading, science, and other academic scores**
        """
                )
        st.subheader("To learn more about the effects of summer and after school programs click [here](https://afterschoolalliance.org/documents/What_Does_the_Research_Say_About_Afterschool.pdf)")
        st_lottie()
    with right_column:
        st_lottie(lottie_graduation,
                  height = 500,
                  width = 500)
    st.divider()

with st.container():
    left_column, right_column = st.columns([4,2.5], gap="medium")
    with left_column:
        st.header("Getting Started")
        st.subheader("Click the button below to advance to the setup wizard so we can find what programs would best fit your child! :point_down:")
        wizard_button = st.button("Navigate to Wizard :mage:", use_container_width=True)
        if wizard_button:
            switch_page("wizard")
    with right_column:
        st_lottie(lottie_search, height = 300, width = 300)



