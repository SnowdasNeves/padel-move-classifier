# -*- coding: utf-8 -*-
import streamlit as st
from streamlit.runtime.scriptrunner.script_run_context import add_script_run_ctx
import threading as th
import paho.mqtt.client as mqtt
from streamlit_autorefresh import st_autorefresh
from streamlit_option_menu import option_menu

# import base64

st.set_page_config(page_title="Padel Move Evaluator", page_icon=":tennis:")

st_autorefresh(interval=1000, key="fizzbuzzcounter")

# con_status tracks the current connection state to MQTT broker
con_status = "Disconnected"


# MQTT Thread Function
def MQTT_TH(client):

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        # Subscribing in on_connect() means that if we lose the connection and reconnect then subscriptions will be renewed
        client.subscribe(st.session_state["MyData"]["TopicSub"])

    # The callback for when a PUBLISH message is received from the server
    def on_message(client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))
        # Store topic and message in session state
        st.session_state["MyData"]["Topic"] = msg.topic
        st.session_state["MyData"]["Message"] = str(msg.payload)

    print("Incializing MQTT")
    client.on_connect = on_connect
    client.on_message = on_message
    st.session_state["MyData"]["Run"] = True
    client.connect(st.session_state["MyData"]["Broker"], 1883, 60)
    client.loop_forever()
    print("MQTT link ended")
    st.session_state["MyData"]["Run"] = False


# Stores states of variables between page refresh
# Data that the progrma uses
if "MyData" not in st.session_state:
    st.session_state["MyData"] = {
        "Run": False,
        "Broker": "",
        "TopicSub": "AAI/#",
        "Topic": "",
        "Message": "",
    }

# MQTT session information
if "mqttThread" not in st.session_state:
    # Open client MQTT connection in an independent thread
    # print('session state')
    st.session_state.mqttClient = mqtt.Client()
    st.session_state.mqttThread = th.Thread(
        target=MQTT_TH, args=[st.session_state.mqttClient]
    )
    # st.session_state.mqttThread = th.Thread(target=MQTT_TH, args=[])
    add_script_run_ctx(st.session_state.mqttThread)
    # st.session_state.mqttThread.start()


## Page design starts here
###############################################################################


def home():
    st.title("Padel Move Evaluator")
    st.write(
        """
             Welcome to the Padel Move Evaluator webpage. To start data
             acquisition establish a connection with the MQTT broker and press
             the 'B' button on the M5Stick!\n
             For further instructions on how to connect to the MQTT broker, if
             you're curious about the methods used in this classifier or want some
             tips to better perform your moves head over to our About & Move List
             page on the sidebar menu.
             """
    )

    st.header("Data Received")
    # Messages to be published
    # topic_reply = 'AAI/padel/start'
    # if st.button('Start acquisition'):
    #     st.session_state.mqttClient.publish(topic_reply, 'start')

    # Display messages received in subscribed topic
    byte_msg = st.session_state["MyData"]["Message"]
    byte_msg = byte_msg[2:-1]
    st.subheader("Your move: " + byte_msg)

    # Insert accelerometer graphs here
    ###########################################################################

    st.text("Data received through: " + st.session_state["MyData"]["Topic"])


def about():
    st.title("About")
    st.write(
        """
             Welcome to the Padel Move Evaluator webpage. This tool was created
             by two NOVA School of Science and Technology students, to help new
             players learn the different moves used in padel and improve their skills.
             """
    )

    st.header("Instructions")
    st.write(
        """
             Start off by going to the MQTT Connection page and confirm the
             connection to the MQTT broker is online.
             You can then run the program from the home page. After pressing the button
             to start the acquisition (button 'B' on the M5Stick), you have 2 seconds
             to do your most impressive padel move. Your move's data will be analyzed by our
             machine learning algorithm! It uses a Random Forest classifier as we
             found it was the one that yielded better accuracy.
             Your results will then be displayed as well as the accelerometer data
             used to classify your move.\n
             You can consult the gifs below to see the available moves as well as
             some tips on how to perform them.\n
             Have fun!
             """
    )

    st.header("Tips & Tricks")

    ## Displays all gifs in About page
    ###########################################################################

    st.write(
        """
            Below you can toggle to see gifs demonstrating all the available moves, in the
            order they are referred to in the subsections.
            """
    )

    st.subheader("Normal Forehand")

    # if st.toggle('See Normal GIF'):
    #     gif_dir = r''
    #     with open(gif_dir, "rb") as gif_file:
    #         base64_encoded = base64.b64encode(gif_file.read()).decode()

    #     st.markdown(
    #         f'<img src="data:image/gif;base64,{base64_encoded}" alt="Normal Forehand" style="width: 150px;">',
    #         unsafe_allow_html=True
    #         )

    st.write(
        """
             Initiate the movement with the racket in a central position, aligned
             with your body. Do the movement as seen on the gif above, keeping in
             mind to do it at a slow pace. The movement ends returning to the
             initial position.
            """
    )
    st.subheader("Backhand")

    # if st.toggle('See Backhand GIF'):
    #     gif_dir = r''
    #     with open(gif_dir, "rb") as gif_file:
    #         base64_encoded = base64.b64encode(gif_file.read()).decode()

    #     st.markdown(
    #         f'<img src="data:image/gif;base64,{base64_encoded}" alt="Backhand" style="width: 150px;">',
    #         unsafe_allow_html=True
    #         )

    st.write(
        """
             Initiate the movement with the racket in a central position, aligned
             with your body. Do the movement as seen on the gif above, keeping in
             mind to do it at a slow pace. The movement ends at the end of the
             follow through.
            """
    )
    st.subheader("Smash")

    # if st.toggle('See Smash GIF'):
    #     gif_dir = r''
    #     with open(gif_dir, "rb") as gif_file:
    #         base64_encoded = base64.b64encode(gif_file.read()).decode()

    #     st.markdown(
    #         f'<img src="data:image/gif;base64,{base64_encoded}" alt="Smash" style="width: 150px;">',
    #         unsafe_allow_html=True
    #         )

    st.write(
        """
             Initiate the movement with the racket in a central position, aligned
             with your body. Do the movement as seen on the gif above. The movement
             until the top position is done at moderate velocity. The smash itself,
             bringing the racket down, is done at high speed. The movement ends
             returning to the initial position.
            """
    )
    st.subheader("Lob")

    # if st.toggle('See Lob GIF'):
    #     gif_dir = r''
    #     with open(gif_dir, "rb") as gif_file:
    #         base64_encoded = base64.b64encode(gif_file.read()).decode()

    #     st.markdown(
    #         f'<img src="data:image/gif;base64,{base64_encoded}" alt="Lob" style="width: 150px;">',
    #         unsafe_allow_html=True
    #         )

    st.write(
        """
             Initiate the movement with the racket in a central position, aligned
             with your body. Do the movement as seen on the gif above, keeping in
             mind to do it at a slow pace. The movement ends at the end of the
             follow through.
            """
    )
    st.subheader("Bandeja")

    # if st.toggle('See Bandeja GIF'):
    #     gif_dir = r''
    #     with open(gif_dir, "rb") as gif_file:
    #         base64_encoded = base64.b64encode(gif_file.read()).decode()

    #     st.markdown(
    #         f'<img src="data:image/gif;base64,{base64_encoded}" alt="Bandeja" style="width: 150px;">',
    #         unsafe_allow_html=True
    #         )

    st.write(
        """
             Initiate the movement with the racket in a central position, aligned
             with your body. Do the movement as seen on the gif above. The movement
             until the top position is done at moderate velocity. The movement to
             hit the ball, bringing the racket down, is done at moderate to high
             speed. The movement ends at the end of the follow through.
            """
    )


def connection():
    global con_status
    st.title("MQTT Comunication")

    # MQTT configuration
    st.session_state["MyData"]["Broker"] = st.text_input("MQTT Broker: ", value="")
    st.session_state["MyData"]["TopicSub"] = st.text_input(
        "Topic subscribed: ", value="AAI/padel/data"
    )

    if st.session_state["MyData"]["Run"]:
        con_status = "Connected"
        if st.button("MQTT disconnect"):
            st.session_state.mqttClient.disconnect()
    else:
        con_status = "Disconnected"
        if st.button("MQTT connect"):
            st.session_state.mqttThread.start()  # Starts thread that controls MQTT

    st.text("Connection status: " + con_status)


# Top or sidebar menu with square frame
with st.sidebar:
    selected_page = option_menu(
        menu_title=None,
        options=["Home", "About & Move List", "MQTT Connection"],
        icons=["house-fill", "info-circle-fill", "router-fill"],
        # orientation="horizontal"
    )

# Radio sidebar already tested
###############################################################################

# selected_page = st.sidebar.radio("Pages", ["Home", "About", "MQTT Connection"])


if selected_page == "Home":
    home()
elif selected_page == "About & Move List":
    about()
elif selected_page == "MQTT Connection":
    connection()

st.markdown(
    """
    <div style="bottom: 0; padding-top: 10px; padding-bottom: 10px; text-align: center">
        <p>© 2023 Padel Move Evaluator Webpage.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
