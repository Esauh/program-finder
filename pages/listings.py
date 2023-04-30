import threading
import cv2
import streamlit as st 
from streamlit_extras.switch_page_button import switch_page
import psycopg2
from streamlit_lottie import st_lottie
import json
from streamlit_webrtc import webrtc_streamer
from deepface import DeepFace

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

if "emotion" not in st.session_state:
    st.session_state["emotion"] = ""

if "program_type" not in st.session_state:
    st.session_state["program_type"] = "Fine Arts"

if "program_time" not in st.session_state:
    st.session_state["program_time"] = "Summer"
    
if "program_date" not in st.session_state:
    st.session_state["program_date"] = "Weekdays"


if st.session_state["program_time"] == "Summer":
    query_pt = 'Summer'
else:
    query_pt = 'School Year'

if st.session_state["program_date"] == "Weekends":
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
    height = 550
    width = 800
elif query_ptype == "Fine Arts":
    lottie = load_lottiefile("lottiefiles/fine_arts.json")
    height = 600
    width = 800
else:
    lottie = load_lottiefile("lottiefiles/multilingual-group.json")
    height = 550
    width = 800
    
def enable_camera():
    st.session_state["camera"] = True

def disable_camera():
    st.session_state["camera"] = False



st.markdown(f"## Here are some :violet[{query_ptype}] programs click the name to view their website :raised_hands:")
st.markdown('''### Additionally we would like to capture emotional data while you view your listings to enable the camera press the :green[Start] button below.''')
    
lock = threading.Lock()
img_container = {"img": None}



face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    with lock:
        img_container["img"] = img
    return frame

ctx = webrtc_streamer(key="example", video_frame_callback=video_frame_callback)

while ctx.state.playing:
    with lock:
        img = img_container["img"]
    if img is None:
        continue
    emotion_data = DeepFace.analyze(img_path=img,actions=['emotion'], enforce_detection="False")
    if emotion_data != []:
        st.session_state["emotion"] = emotion_data[0]["dominant_emotion"]

st.markdown("### :point_up_2: You will not be able to navigate to another page until you press the :red[Stop] button and disable the camera")
st.divider()

with st.container():
    left_column, right_column = st.columns([1,1.5],gap="large")
    rank = 1
    with left_column:
        for row in rows:
            st.markdown(f"""
            ### :violet[Program {rank}:] [{row[6]}]({row[4]})
            #### :orange[Costs: ${row[5]}]
            """)
            st.divider()
            rank += 1
    with right_column:
        st_lottie(lottie, height =height, width=width)

#row[1] = School Year or Summer
#row[2] = Weekdays or Weekends
#row[3] = Stem or Foreign Language or Fine Arts
#row[4] = Website link
#row[5] = Cost of program
#row[6] = Name of program

with st.container():
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


