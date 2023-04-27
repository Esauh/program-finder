import streamlit as st 
from streamlit_extras.switch_page_button import switch_page

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

st.header("Program Listings Coming Soon!")
with st.container():
    st.write("##")
    st.write("To return to the welcome page click the button below")
    return_home = st.button("Return to Home page")
    if return_home:
        switch_page("welcome")
